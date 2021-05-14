import React, { useEffect, useState } from "react";
import styled from "./employees.module.css";
import axiosInstance from "../../api/axios";

export const Employees = () => {
  const [employees, setEmployees] = useState([]);
  const [filteredEmployees, setFilteredEmployees] = useState([]);
  const [searchFirstname, setSearchFirstname] = useState("");
  const [searchLastname, setSearchLastname] = useState("");
  const [loading, setLoading] = useState(true);
  const [employeeData, setEmployeeData] = useState("");
  const [totalMessages, setTotalMessages] = useState("");

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

  useEffect(() => {
    if (employees.length !== 0) {
      setFilteredEmployees(
        employees.filter(
          (e) =>
            e.lastname.toLowerCase().includes(searchLastname.toLowerCase()) &&
            e.firstname.toLowerCase().includes(searchFirstname.toLowerCase())
        )
      );
    }
  }, [searchLastname, searchFirstname, employees]);

  const handleClick = (eid) => {
    alert("wait 20 seks. efficiency not important");
    axiosInstance
      .post(
        "employees/get_employee_info",
        {
          data: {
            eid: eid,
          },
        },
        {
          headers: {
            "x-access-token": localStorage.getItem("token"),
          },
          timeout: 28000,
        }
      )
      .then((res) => {
        setEmployeeData([]);
        setEmployeeData(res.data);
        setTotalMessages(res.data.reverse()[0]["totalMessages"]);
      })
      .catch((e) => {
        console.log(e);
        alert(e);
      });
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
        {employeeData === "" ? (
          <h1>No employe selected</h1>
        ) : (
          <div>
            <h1>Total messages sent: {totalMessages}</h1>
            <ul>
              {employeeData.map((object, index) => {
                return (
                  <li key={index}>
                    <p>{object.employee}</p>
                  </li>
                );
              })}
            </ul>
          </div>
        )}
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
