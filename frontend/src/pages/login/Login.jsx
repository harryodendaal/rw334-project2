import React from 'react';
import {Formik} from 'formik';
import * as Yup from 'yup';
import axiosInstance from '../../api/axios'
import {useHistory} from 'react-router-dom'
const loginValidation =  Yup.object().shape({
  username: Yup.string().required("Email is required"),
  password: Yup.string()
  .required("Password is required")
  .min(12 ,"password needs to be atleast 12 characters long")
})

export const Login = () => {
  const history = useHistory();
  return (
    <div>
      <h1>Login</h1>
      <Formik
      validationSchema={loginValidation}
        initialValues={{username:"", password:""}}
        onSubmit={(values) => {
          console.log(values)

          axiosInstance
            .post("login", {
              username:values.username,
              password: values.password
            })
            .then((res) => {
              localStorage.setItem('token', res.data['token'])
              history.push('/')
            }).catch((e) => {
              console.log(e)
              alert(e)
            })

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
          <button type='submit'>
            Submit
          </button>
        </form>
      )}

      </Formik>
    </div>
  )
}
