export const translateDescription = (desc) => {
  const turkishToEnglishKeyMap = {
    "Ekran Boyutu": "display_size",
    "Ekran Teknolojisi": "display_technology",
    "Piksel Yoğunluğu": "ppi_density",
    "Batarya Kapasitesi": "battery",
    "Kamera Çözünürlüğü": "camera_resolution",
    "CPU Üretim Teknolojisi": "cpu_manufacturing",
    "İşletim Sistemi": "os",
    "RAM Kapasitesi": "ram",
    "Dahili Hafıza": "storage",
    "Hızlı Şarj Desteği": "fast_charging",
    "Ekran Yenileme Hızı": "refresh_rate",
    "5G": "5g",
    Price: "price",
  };

  if (!desc) return [];

  const pairs = desc
    .split(";")
    .map((p) => p.trim())
    .filter(Boolean);

  const pairSlice = pairs.slice(0, -1);

  return pairSlice
    .map((pair) => {
      const [turkishKey, value] = pair.split(":").map((s) => s.trim());
      if (!turkishKey || !value) return null;

      const key = turkishToEnglishKeyMap[turkishKey] || turkishKey;
      return { key, value };
    })
    .filter(Boolean);
};

export const getDisplayLabel = (key) => {
  const keyMap = {
    storage: "Storage",
    ram: "RAM",
    phone_brand: "Brand",
    phone_model: "Model",
    dimensions: "Dimensions",
    display_size: "Display Size",
    display_technology: "Display Technology",
    display_resolution: "Display Resolution",
    os: "Operating System",
    battery: "Battery",
    video: "Video",
    chipset: "Chipset",
    cpu: "Processor",
    cpu_manufacturing: "CPU Manufacturing",
    gpu: "Graphics Processor",
    ppi_density: "PPI Density",
    camera_resolution: "Camera Resolution",
    fast_charging: "Fast Charging",
    refresh_rate: "Refresh Rate",
    "5g": "5G",
    price: "Price",
  };

  return (
    keyMap[key] ||
    key.replace(/_/g, " ").replace(/\b\w/g, (l) => l.toUpperCase())
  );
};

export const formatValue = (key, value) => {
  switch (key) {
    case "storage":
    case "ram":
      return value.toUpperCase().includes("GB") ? value : `${value} GB`;
    case "battery":
      return value.toUpperCase().includes("MAH") ? value : `${value} mAh`;
    case "display_size":
      return value.includes("İnç") ? value.replace("İnç", "inch") : `${value}`;
    case "ppi_density":
      return value.toUpperCase().includes("PPI") ? value : `${value} PPI`;

    case "fast_charging":
    case "5g":
      return value.toLowerCase() === "var" ? "Yes" : "No";
    default:
      return value;
  }
};
