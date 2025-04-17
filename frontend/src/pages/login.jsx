import { useState } from "react";
import "./login.css";
import { useNavigate } from "react-router-dom";
import { UserApi } from "../utils/requests";
import swal from 'sweetalert';

const Login = () => {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const navigate = useNavigate();

  const captureChanges = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };
  const saveChanges = async (e) => {
    e.preventDefault();
    UserApi.login(formData)
      .then((data) => {
        swal('Success', 'Successfully Logged In', 'success');
        localStorage.setItem("token", data.access);
        UserApi.info()
          .then((data) => {
            console.log(data);
            localStorage.setItem("id", data.id);
            localStorage.setItem("username", data.username);
          })
          .then(() => {
            setTimeout(() => {
              navigate("/dashboard");
            }, 2000);
          });
      })
      .catch(async (error) => {
        console.error("Error:", error);
        swal('Error', error.detail, 'error');
        console.log("Login Unsuccessful");
      });
  };

  return (
    <div className="pageBody">
      <div className="myCard">
        <div className="card-body" style={{ padding: "20px" }}>
          <h3 className="card-title">Login</h3>
          <form onSubmit={saveChanges}>
            <div className="mb-3">
              <label htmlFor="email" className="form-label">
                Email address
              </label>
              <input
                type="email"
                className="form-control"
                name="email"
                value={formData.email}
                placeholder="Enter your email address"
                onChange={captureChanges}
                required
              />
            </div>
            <div className="mb-3">
              <label htmlFor="password" className="form-label">
                Password
              </label>
              <input
                type="password"
                className="form-control"
                name="password"
                value={formData.password}
                placeholder="Enter your password"
                onChange={captureChanges}
                required
              />
            </div>
            <button type="submit" className="btn btn-primary">
              Login
            </button>
            <p></p>
            <a href="http://localhost:5173/register">
              <p>Create new account</p>
            </a>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Login;
