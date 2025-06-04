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
    console.log("Ürünler:", response.data);
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

export const getProductById = async (id) => {
  try {
    const response = await api.get(`/api/Product/getProductById/${id}`);
    console.log(response.data);
    return response.data;
  } catch (error) {
    console.error("Ürün getirme hatası:", error);
    throw error;
  }
};

export const addFavoriteProduct = async (userId, productId) => {
  try {
    const response = await api.post('api/FavoriteProduct/addFavoriteProduct', {
      userId: userId,
      productId: productId
    });

    if (response.data === true) {
      console.log('Ürün favorilere eklendi.');
    } else {
      console.log('Ürün zaten favorilerde.');
    }
  } catch (error) {
    if (error.response && error.response.status === 404) {
      console.error('Kullanıcı veya ürün bulunamadı.');
    } else {
      console.error('Bir hata oluştu:', error.message);
    }
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

export const getUserFromId = async (id) => {
  try {
    const response = await api.get(`/api/Auth/getUserFromId?id=${id}`);
    console.log("Kullanıcı bilgisi:", response);
    return response.data;
  } catch (error) {
    console.error("Kullanıcı alınırken hata oluştu:", error);
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
