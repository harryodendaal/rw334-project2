import React from "react";
import styled from "./employees.module.css";
import { Formik } from "formik";

export const Employees = () => {
  return (
    <div className={styled.container}>
      <div className={styled.border}>
        <h2>Search for Employee</h2>
        <Formik initialValues={{ username: "", password }}></Formik>
      </div>
    </div>
  );
};
