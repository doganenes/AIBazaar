import axios from "axios";

const BACKEND_API_BASE_URL = "https://localhost:7011";
const AI_API_BASE_URL = "http://localhost:8000";

const api = axios.create({
  baseURL: BACKEND_API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

const aiApi = axios.create({
  baseURL: AI_API_BASE_URL,
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
    console.log("Products:", response.data);
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
    console.log("Favorites:", response.data);
    return response.data;
  } catch (error) {
    console.error("API error:", error.message);
    return [];
  }
};

export const getProductById = async (id) => {
  try {
    const response = await api.get(`/api/Product/getProductById/${id}`);
    console.log("Product:", response.data);
    return response.data;
  } catch (error) {
    console.error("Error:", error);
    throw error;
  }
};

const searchProducts = async (searchDto) => {
  try {
    const response = await api.post("/api/products/searchProducts", searchDto);
    return response.data;
  } catch (error) {
    console.error("Product search failed:", error);
    throw error;
  }
};

export const addFavoriteProduct = async (userId, productId) => {
  try {
    const response = await api.post("/api/FavoriteProduct/addFavoriteProduct", {
      userId,
      productId,
    });
    return response.data;
  } catch (error) {
    const errorMessage =
      error.response?.data?.error || "Error adding to favorites.";
    throw new Error(errorMessage);
  }
};

export const removeFavoriteProduct = async (userId, productId) => {
  try {
    const response = await api.delete(
      `/api/FavoriteProduct/removeFavoriteProduct`,
      {
        data: {
          userId: userId,
          productId: productId,
        },
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

export const predict_knn = async (formData) => {
  try {
    const response = await aiApi.post("/api/predict/", formData);
    return response.data;
  } catch (error) {
    console.error("API error occurred:", error);
    throw error;
  }
};

export const getUserFromId = async (id) => {
  try {
    const response = await api.get(`/api/Auth/getUserFromId?id=${id}`);
    console.log("User info:", response);
    return response.data;
  } catch (error) {
    console.error("Error fetching user:", error);
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
