import React from 'react';
import {Formik} from 'formik';
import * as Yup from 'yup';


const regValidation =  Yup.object().shape({
  username: Yup.string().required("Email is required"),
  password: Yup.string()
  .required("Password is required")
  .min(12 ,"password needs to be atleast 12 characters long")
})

export const register = () => {
  return (
    <div>
    <h1>Register</h1>
    <Formik
    validationSchema={regValidation}
      initialValues={{username:"", password:""}}
      onSubmit={(values) => {
        console.log(values)

      }}
    >{({
      values,
      errors,
      touched,
      handleSubmit,
      handleChange,
      handleBlur,
      isSubmitting
      
    }) => (
      <form onSubmit={handleSubmit}>
        <input
          type='text'
          name='username'
          onChange={handleChange}
          onBlur={handleBlur}
          value={values.username}
        />
        {values.username && touched.username && errors.username}
        <input
          type="password"
          name="password"
          onChange={handleChange}
          onBlur={handleBlur}
          value={values.password}
        />
        {errors.password && touched.password && errors.password}
        <button type='submit' disabled={isSubmitting}>
          Submit
        </button>
      </form>
    )}

    </Formik>
  </div>
  )
}
