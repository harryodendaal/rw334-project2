import * as d3 from 'd3'

export const drawGraph = (data, visType) => {
    if ('nodes' in data) {
      let svg = d3.select("svg");
      d3.select(".viz")
      .call(d3.zoom().on("zoom", function (event) {
        svg.attr("transform", event.transform)
      }));
      const width = svg.attr("width");
      const height = svg.attr("height");

      let graphData = data;
      let pathNodes = [];    
      
      // Shortest path
      if (visType === 'shortest-path') {
        pathNodes = graphData['path_nodes'];
      }
      let drag = simulation => {
    
        function dragstarted(event) {
          if (!event.active) simulation.alphaTarget(0.3).restart();
          event.subject.fx = event.subject.x;
          event.subject.fy = event.subject.y;
        }
        
        function dragged(event) {
          event.subject.fx = event.x;
          event.subject.fy = event.y;
        }
        
        function dragended(event) {
          if (!event.active) simulation.alphaTarget(0);
          event.subject.fx = null;
          event.subject.fy = null;
        }
        
        return d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended);
      }

      const simulation = d3.forceSimulation(graphData.nodes)
            .force("link", d3.forceLink(graphData.links).id(d => d.id))
            .force("charge", d3.forceManyBody())
            .force("center", d3.forceCenter(width / 2, height / 2));

      simulation.on("tick", () => {
        link
            .attr("x1", d => d.source.x)
            .attr("y1", d => d.source.y)
            .attr("x2", d => d.target.x)
            .attr("y2", d => d.target.y);

        node
            .attr("cx", d => d.x)
            .attr("cy", d => d.y);
      });

      const link = svg.append("g")
            .selectAll("line")
            .data(graphData.links)
            .enter()
            .append("line")
            // .join("line")
            .attr("stroke-width", d => Math.sqrt(d.value))
            .attr("stroke-opacity", 0.6)
            .attr("stroke", e => {
              // Shortest path
              if (visType === 'shortest-path') {
                if (pathNodes.includes(e.source.id)) {
                  let sourceIndex = pathNodes.findIndex(node => {return node === e.source.id});
                  if (sourceIndex <= pathNodes.length ) {
                    if (pathNodes[sourceIndex + 1] === e.target.id) {
                      return "green";
                    } else if (pathNodes[sourceIndex - 1] === e.target.id) {
                      return "green";
                    }
                  }
                  
                } else if (pathNodes.includes(e.target.id)) {
                  let targetIndex = pathNodes.findIndex(node => {return node === e.target.id});
                  if (targetIndex <= pathNodes.length ) {
                    if (pathNodes[targetIndex + 1] === e.source.id) {
                      return "green";
                    } else if (pathNodes[targetIndex - 1] === e.source.id) {
                      return "green";
                    }
                  }
                }
              }
              return "#999";
            });

      // Label propagation
      function getRandomColor() {
        var letters = '0123456789ABCDEF';
        var color = '#';
        for (var i = 0; i < 6; i++) {
          color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
      }

      // Generate random colours
      let community_colours = {};
      
      if (visType === 'label-propagation') {
        graphData.nodes.forEach(element => {
          if (!(element.communityId.toString() in community_colours)) {
            community_colours[element.communityId.toString()] = getRandomColor();
          }
        });
      }
      

      const node = svg.append("g")
            .attr("stroke", "#fff")
            .attr("stroke-width", 1.5)
            .selectAll("circle")
            .data(graphData.nodes)
            .enter()
            .append("circle")
            // .join("circle")
            .attr("r", 5)
            .attr("fill",  function (d) { 
              // Shortest path
              if(visType === 'shortest-path') {
                if(pathNodes.includes(d.id)) {
                  return "#ff00f2";
                } else {
                  return "black";
                }
              }
              // Centrality
              if(visType === 'centrality') {
                let score_color = (d.score - 2 / (4.34 - 2)) * 255;
                if (score_color < 0) {
                  score_color = 0;
                }
                let color = 40 + score_color;
                return 'rgb(' + color + ',' + 100 + ',' + (150-color) + ')';
              }
              // Label propagation
              if(visType === 'label-propagation') {
                return community_colours[d.communityId.toString()];
              }
              return "blue";
            })
            .call(drag(simulation));

      if (visType === 'social-network') {
        node.append("title")
            .text(d => d.firstname + ' ' + d.lastname);
      } else if (visType === 'centrality') {
        node.append("title")
            .text(d => 'Email: ' + d.emailaddress + '\nScore: ' + d.score.toFixed(2));
      } else { 
        node.append("title")
            .text(d => 'Email: ' + d.emailaddress);
      }
      
    } else {
      return
    }
}