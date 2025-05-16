import axios from "axios";

const API_BASE_URL = "https://localhost:7011";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export const register = async (formData) => {
  try {
    const response = await api.post("/api/Auth/Register", formData);
    return response.data;
  } catch (error) {
    if (error.response) {
      return error.response.data;
    }
    throw new Error("Network error occurred.");
  }
};

export const login = async (formData) => {
  try {
    console.log(`Form datamız: ${formData}`)
    const response = await api.post("/api/Auth/login", formData);
    console.log(`Bizim dönen response : ${response.data}`)
    return response.data;
  } catch (error) {
    if (error.response) {
      return error.response.data;
    }
    throw new Error("Network error occurred.");
  }
};

export const tokenToId = async () => {
  const token = localStorage.getItem("authToken");
  if (!token) {
    throw new Error("No token found. Please log in.");
  }

  try {
    const { data: tokenResponse } = await api.get("/api/auth/tokenToId", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    console.log("Token response:", tokenResponse);
    return tokenResponse;
  } catch (error) {
    console.error("Error fetching token to ID:", error);
    throw new Error(`${error}`);
  }
};