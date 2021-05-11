import React, { useEffect } from "react";
import axios from "axios";
import * as d3 from "d3";
import { drawGraph } from "./drawGraph";

export const Graph = (props) => {
  useEffect(() => {
    if (props.visType === "social-network") {
      d3.selectAll("svg > *").remove();
    } else if (props.visType === "label-propagation") {
      d3.selectAll("svg > *").remove();
    } else if (props.visType === "shortest-path") {
      d3.selectAll("svg > *").remove();
    } else if (props.visType === "centrality") {
      d3.selectAll("svg > *").remove();
    } else {
      return;
    }

    let apiLink = "http://127.0.0.1:5000/graphs/";

    if (props.visType !== "social-network") {
      apiLink = apiLink + props.visType;
    }

    axios
      .get(
        apiLink,
        { timeout: 14000 },
        {
          headers: {
            "x-access-token": localStorage.getItem("token"),
          },
        }
      )
      .then((res) => {
        drawGraph(res.data, props.visType);
      })
      .catch((e) => {
        console.log(e);
        alert(e);
      });
  });

  const zoomStyles = {
    overflow: "hidden",
  };

  return (
    <div>
      <h1>{props.visType}</h1>
      <div style={zoomStyles}>
        <div className="viz">
          <svg width="1650" height="1550"></svg>
        </div>
      </div>
    </div>
  );
};
