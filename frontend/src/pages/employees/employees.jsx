import React, { useEffect, useState } from "react";
import styled from "./employees.module.css";
import axiosInstance from "../../api/axios";

export const Employees = () => {
  const [employees, setEmployees] = useState([]);
  const [filteredEmployees, setFilteredEmployees] = useState([]);
  const [searchFirstname, setSearchFirstname] = useState("");
  const [searchLastname, setSearchLastname] = useState("");
  const [loading, setLoading] = useState(true);
  function removeNull(array) {
    return array.filter((x) => x.firstname !== null);
  }

  useEffect(() => {
    axiosInstance
      .get("employees/allemployees", {
        headers: {
          "x-access-token": localStorage.getItem("token"),
        },
      })
      .then((res) => {
        setEmployees(removeNull(res.data));
        setLoading(false);
      })
      .catch((e) => {
        console.log(e);
        alert(e);
        // alert(e.response.data["message"]);
      });
  }, []);

  useEffect(() => {
    if (employees.length !== 0) {
      setFilteredEmployees(
        employees.filter((e) =>
          e.firstname.toLowerCase().includes(searchFirstname.toLowerCase())
        )
      );
    }
  }, [searchFirstname, employees]);

  useEffect(() => {
    if (employees.length !== 0) {
      setFilteredEmployees(
        employees.filter((e) =>
          e.lastname.toLowerCase().includes(searchLastname.toLowerCase())
        )
      );
    }
  }, [searchLastname, employees]);

  const handleClick = (eid) => {
    console.log(eid);
    // axiosInstance
    //   .post("employees/newendpoint", {
    //     headers: {
    //       "x-access-token": localStorage.getItem("token"),
    //     },
    //   })
    //   .then((res) => {
    //     console.log(res);
    //   })
    //   .catch((e) => {
    //     console.log(e);
    //     alert(e);
    //   });
  };
  if (loading) {
    return <p>Loading Employees...</p>;
  }

  return (
    <div>
      <div className={styled.container}>
        <div className={styled.border}>
          <h2>Search for Employee</h2>

          <b>firstname</b>
          <input
            type="text"
            placeholder="Search firstnames"
            onChange={(e) => setSearchFirstname(e.target.value)}
          />
          <b>Lastname</b>
          <input
            type="text"
            placeholder="Search Lastname"
            onChange={(e) => setSearchLastname(e.target.value)}
          />
        </div>
      </div>
      <div className={styled.container}>
        <h2>All Employees:</h2>
        <div className={styled.employees}>
          {filteredEmployees?.map(({ firstname, lastname, eid }) => (
            <div className={styled.border}>
              <div key={eid}>
                <h1>{firstname}</h1>
                <h2>{lastname}</h2>
              </div>
              <button onClick={() => handleClick(eid)}>My data</button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
