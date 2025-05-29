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
    const response = await api.post("/api/Auth/login", formData);
    console.log("API'den dönen yanıt:", response.data);

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
    const { data } = await api.get(`/api/auth/getIdFromToken?t=${token}`);
    console.log("Token response:", data);
    return data.user;
  } catch (error) {
    console.error("Error fetching token to ID:", error);
    throw new Error("Favori ürünler alınamadı: " + error);
  }
};

export const getAllProducts = async () => {
  try {
    const response = await api.get("/api/product/getAllProducts");
    return response.data;
  } catch (error) {
    console.error("Error fetching products:", error);
    throw new Error("Failed to fetch products.");
  }
};

export const getAllFavoriteProducts = async (userId) => {
  try {
    const response = await api.get(
      `/api/FavoriteProduct/getAllFavoriteProducts?id=${userId}`,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("authToken")}`,
        },
      }
    );
    console.log("Favori ürünler:", response.data);
    return response.data;
  } catch (error) {
    console.error("API hatası:", error.message);
    return [];
  }
};

export const addFavoriteProduct = async (userId, productId) => {
  try {
    const response = await api.post(
      `/api/FavoriteProduct/addFavoriteProduct`,
      { userId, productId },
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("authToken")}`,
        },
      }
    );
    return response.data;
  } catch (error) {
    if (error.response) return error.response.data;
    throw new Error("Network error occurred.");
  }
};

export const removeFavoriteProduct = async (userId, productId) => {
  try {
    const response = await api.delete(
      `/api/FavoriteProduct/removeFavoriteProduct`,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("authToken")}`,
        },
        data: { userId, favoriteProductId: productId },
      }
    );
    return response.data;
  } catch (error) {
    if (error.response) return error.response.data;
    throw new Error("Network error occurred.");
  }
};

export const predict_knn = async (formData) => {
  try {
    const response = await axios.post(
      "http://localhost:8000/api/predict/",
      formData
    );
    return response.data;
  } catch (error) {
    console.error("API çağrısı sırasında hata oluştu:", error);
    throw error;
  }
};

export const logout = async () => {
  try {
    localStorage.removeItem("authToken");
    return { message: "Logout successful" };
  } catch (error) {
    console.error("Logout error:", error);
    throw new Error("Logout failed");
  }
};