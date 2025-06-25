import React from "react";
import { Navigate, Outlet } from "react-router-dom";

function PrivateRoute() {
  const token = localStorage.getItem("authToken");

  if (!token) {
    return <Navigate to="/signin" replace />;
  }

  return <Outlet />;
}

export default PrivateRoute;