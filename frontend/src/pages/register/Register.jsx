import React from "react";
import { Formik } from "formik";
import * as Yup from "yup";
import styled from "./register.module.css";
import axiosInstance from "../../api/axios";
import { useHistory } from "react-router-dom";

const regValidation = Yup.object().shape({
  username: Yup.string().required("Email is required"),
  password: Yup.string()
    .required("Password is required")
    .min(12, "password needs to be atleast 12 characters long"),
});

export const Register = ({ changeToken }) => {
  const history = useHistory();
  return (
    <div className={styled.container}>
      <div className={styled.border}>
        <h2>Register</h2>
        <Formik
          validationSchema={regValidation}
          initialValues={{ username: "", password: "" }}
          onSubmit={(values) => {
            console.log(values);
            axiosInstance
              .post("register", {
                username: values.username,
                password: values.password,
              })
              .then((res) => {
                console.log(res);
                localStorage.setItem("token", res.data["access_token"]);
                history.push("/");
                changeToken();
              })
              .catch((e) => {
                console.log(e);
                alert(e.response.data['message']);
              });
          }}
        >
          {({
            values,
            errors,
            touched,
            handleSubmit,
            handleChange,
            handleBlur,
            isSubmitting,
          }) => (
            <form onSubmit={handleSubmit}>
              <p>
                Username:
              </p>
              <input
                className={styled.input}
                type="text"
                name="username"
                onChange={handleChange}
                onBlur={handleBlur}
                value={values.username}
              />
              {values.username && touched.username && errors.username}
              <p>
                Password:
              </p>
              <input
                className={styled.input}
                type="password"
                name="password"
                onChange={handleChange}
                onBlur={handleBlur}
                value={values.password}
              />
              {errors.password && touched.password && errors.password}
              <button type="submit" disabled={isSubmitting}>
                Submit
              </button>
            </form>
          )}
        </Formik>
      </div>
    </div>
  );
};
