import React, { useState } from "react";
import "./App.css";
import api from "./services/api";

function App() {
  const [page, setPage] = useState("dashboard");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [token, setToken] = useState("");
  const [image, setImage] = useState(null);
  const [result, setResult] = useState("");
  const [analytics, setAnalytics] = useState(null);
  const [submissions, setSubmissions] = useState([]);

  async function login() {
    try {
      const response = await api.post("/auth/login", {
        email,
        password
      });

      setToken(response.data.access_token);

      alert("Login Successful");
    } catch (error) {
      console.error(error);
      alert("Login Failed");
    }
  }

  function logout() {
    setToken("");
    setEmail("");
    setPassword("");
    setSubmissions([]);
    setAnalytics(null);

    alert("Logged Out");
  }

  async function uploadImage() {

    if (!token) {
      alert("Please login first");
      return;
    }

    if (!image) {
      alert("Please select an image");
      return;
    }

    const formData = new FormData();
    formData.append("images", image);

    try {

      const response = await api.post(
        "/submissions/upload",
        formData,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "multipart/form-data"
          }
        }
      );

      setResult(
        JSON.stringify(
          response.data,
          null,
          2
        )
      );

      alert("Upload Successful");

    } catch (error) {
      console.error(error);
      alert("Upload Failed");
    }
  }

  async function loadAnalytics() {

    try {

      const response =
        await api.get(
          "/analytics/dashboard"
        );

      setAnalytics(
        response.data
      );

    } catch (error) {

      console.error(error);

      alert(
        "Failed to load analytics"
      );
    }
  }

  async function loadMySubmissions() {

    if (!token) {
      alert("Please login first");
      return;
    }

    try {

      const response =
        await api.get(
          "/submissions/my",
          {
            headers: {
              Authorization:
                `Bearer ${token}`
            }
          }
        );

      setSubmissions(
        response.data
      );

    } catch (error) {

      console.error(error);

      alert(
        "Failed to load submissions"
      );
    }
  }

  return (
    <div>

      <div className="navbar">

        <h1>
          AI Content Moderation Platform
        </h1>

        <div className="nav-buttons">

          <button
            onClick={() =>
              setPage("dashboard")
            }
          >
            Dashboard
          </button>

          <button
            onClick={() =>
              setPage("upload")
            }
          >
            Upload
          </button>

          <button
            onClick={() =>
              setPage("analytics")
            }
          >
            Analytics
          </button>

          <button
            onClick={() =>
              setPage("history")
            }
          >
            History
          </button>

        </div>

      </div>

      <div className="container">

        {page === "dashboard" && (

          !token ? (

            <div className="section-card">

              <h2>Login</h2>

              <input
                className="input"
                type="email"
                placeholder="Email"
                value={email}
                onChange={(e) =>
                  setEmail(
                    e.target.value
                  )
                }
              />

              <br /><br />

              <input
                className="input"
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) =>
                  setPassword(
                    e.target.value
                  )
                }
              />

              <br /><br />

              <button
                className="primary-btn"
                onClick={login}
              >
                Login
              </button>

            </div>

          ) : (

            <div className="section-card">

              <h2>
                Welcome Imran Nadeem
              </h2>

              <p>
                <strong>Email:</strong>
                {" "}
                {email}
              </p>

              <p>
                <strong>Status:</strong>
                {" "}
                Logged In
              </p>

              <p>
                <strong>Authentication:</strong>
                {" "}
                JWT Active
              </p>

              <p>
                <strong>Backend:</strong>
                {" "}
                Connected
              </p>

              <p>
                <strong>Database:</strong>
                {" "}
                MongoDB Connected
              </p>

              <br />

              <button
                className="primary-btn"
                onClick={logout}
              >
                Logout
              </button>

            </div>

          )
        )}

        {page === "upload" && (

          <div className="section-card">

            <h2>
              Upload Image
            </h2>

            <input
              type="file"
              accept="image/*"
              onChange={(e) =>
                setImage(
                  e.target.files[0]
                )
              }
            />

            <br /><br />

            <button
              className="primary-btn"
              onClick={uploadImage}
            >
              Upload Image
            </button>

            <br /><br />

            <textarea
              rows="12"
              cols="100"
              value={result}
              readOnly
            />

          </div>
        )}

        {page === "analytics" && (

          <div>

            <button
              className="primary-btn"
              onClick={loadAnalytics}
            >
              Load Analytics
            </button>

            <br /><br />

            {analytics && (

              <div className="analytics-grid">

                <div className="analytics-card">
                  <h3>Total Users</h3>
                  <h1>
                    {analytics.total_users}
                  </h1>
                </div>

                <div className="analytics-card">
                  <h3>Total Submissions</h3>
                  <h1>
                    {analytics.total_submissions}
                  </h1>
                </div>

                <div className="analytics-card">
                  <h3>Approved</h3>
                  <h1>
                    {analytics.approved_submissions}
                  </h1>
                </div>

                <div className="analytics-card">
                  <h3>Blocked</h3>
                  <h1>
                    {analytics.blocked_submissions}
                  </h1>
                </div>

                <div className="analytics-card">
                  <h3>Appeals</h3>
                  <h1>
                    {analytics.total_appeals}
                  </h1>
                </div>

                <div className="analytics-card">
                  <h3>Violence Detections</h3>
                  <h1>
                    {
                      analytics.graphic_violence_detections
                    }
                  </h1>
                </div>

              </div>

            )}

          </div>
        )}

        {page === "history" && (

          <div className="section-card">

            <h2>
              Submission History
            </h2>

            <button
              className="primary-btn"
              onClick={
                loadMySubmissions
              }
            >
              Load My Submissions
            </button>

            <br /><br />

            <table>

              <thead>

                <tr>
                  <th>ID</th>
                  <th>Name</th>
                  <th>Outcome</th>
                  <th>Email</th>
                </tr>

              </thead>

              <tbody>

                {submissions.map(
                  (submission) => (

                    <tr
                      key={
                        submission._id
                      }
                    >
                      <td>
                        {submission._id}
                      </td>

                      <td>
                        {
                          submission.name ||
                          "Unknown"
                        }
                      </td>

                      <td>

                        <span
                          className={
                            submission.outcome === "Approved"
                              ? "badge-approved"
                              : submission.outcome === "Blocked"
                              ? "badge-blocked"
                              : "badge-flagged"
                          }
                        >
                          {
                            submission.outcome
                          }
                        </span>

                      </td>

                      <td>
                        {
                          submission.email
                        }
                      </td>

                    </tr>

                  )
                )}

              </tbody>

            </table>

          </div>

        )}

      </div>

    </div>
  );
}

export default App;