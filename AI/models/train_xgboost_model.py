import pandas as pd
import xgboost as xgb
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import os


class PhonePricePredictionModel:
    def __init__(self, csv_path=None):
        self.csv_path = csv_path or r"C:\Users\pc\Desktop\AIbazaar\AIBazaar\AI\utils\notebooks\product_specs_en.csv"
        self.model = None
        self.scaler = StandardScaler()
        self.feature_columns = [
            "RAM",
            "Storage",
            "Display Size",
            "Battery Capacity",
            "Quick Charge",
            "Pixel Density",
            "os_encoded",
            "display_type_encoded",
            "camera",
            "CPU Manufacturing",
        ]

        # Hierarchy mappings
        self.os_hierarchy = {
            "HarmonyOS": 1,
            "EMUI": 2,
            "Android": 3,
            "iOS": 4,
        }

        self.display_type_hierarchy = {
            "PLS LCD": 1,
            "IPS LCD": 2,
            "OLED": 3,
            "AMOLED": 4,
            "Super AMOLED": 5,
            "Dynamic LTPO AMOLED 2X": 6,
            "Super Retina XDR OLED": 7,
            "LTPO Super Retina XDR OLED": 8,
            "Other": 0,
        }

        self.df = None
        self.is_trained = False

    def safe_map(self, value, mapping, default=0):
        """Safely map values using hierarchy mappings"""
        return mapping.get(value, default)

    def load_and_preprocess_data(self):
        """Load and preprocess the dataset"""
        try:
            # Load data
            self.df = pd.read_csv(self.csv_path)

            # Select required features
            features = [
                "RAM",
                "Storage",
                "Display Size",
                "Battery Capacity",
                "Quick Charge",
                "Pixel Density",
                "Operating System",
                "Display Technology",
                "camera",
                "CPU Manufacturing",
            ]
            self.df = self.df[features + ["price", "Model"]]

            # Encode OS types
            self.df["os_encoded"] = self.df["Operating System"].apply(
                lambda x: self.safe_map(x, self.os_hierarchy)
            )

            # Clean and encode display types
            self.df["Display Technology"] = self.df["Display Technology"].apply(
                lambda x: x.split(",")[0].strip() if isinstance(x, str) else x
            )
            self.df["display_type_encoded"] = self.df["Display Technology"].apply(
                lambda x: self.safe_map(x, self.display_type_hierarchy)
            )

            # Process chipset data
            self.df["CPU Manufacturing"] = self.df["CPU Manufacturing"].apply(
                self._process_chipset
            )

            return True

        except Exception as e:
            print(f"Error loading data: {str(e)}")
            return False

    def _process_chipset(self, x):
        """Process chipset information to extract nm value"""
        try:
            if isinstance(x, str) and "(" in x and "nm" in x:
                return int(
                    "".join(filter(str.isdigit, x.split("(")[-1].split("nm")[0]))
                )
            return 0
        except:
            return 0

    def train_model(self):
        """Train the XGBoost model"""
        if self.df is None:
            if not self.load_and_preprocess_data():
                raise Exception("Failed to load and preprocess data")

        # Prepare features and target
        X = self.df[self.feature_columns]
        y = self.df["price"]

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Initialize and train model
        self.model = xgb.XGBRegressor(
            objective="reg:squarederror",
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            random_state=42,
            subsample=0.8,
            colsample_bytree=0.8,
            reg_alpha=0.1,
            reg_lambda=0.1,
        )

        self.model.fit(X_train, y_train)
        self.is_trained = True

        # Calculate and return training metrics
        train_score = self.model.score(X_train, y_train)
        test_score = self.model.score(X_test, y_test)

        return {
            "train_score": train_score,
            "test_score": test_score,
            "training_samples": len(X_train),
            "test_samples": len(X_test),
        }

    def predict_price(self, phone_specs):
        """
        Predict phone price based on specifications

        Args:
            phone_specs (dict): Dictionary containing phone specifications
                - RAM (float): RAM in GB
                - Storage (float): Storage in GB
                - Display Size (float): Display size in inches
                - Battery Capacity (float): Battery capacity in mAh
                - Quick Charge (int): Quick charge support (0 or 1)
                - Pixel Density (int): PPI density
                - Operating System (str): Operating system type
                - Display Technology (str): Display technology type
                - camera (float): Camera megapixels
                - CPU Manufacturing (int): CPU manufacturing process in nm

        Returns:
            dict: Prediction results including price, encodings, and model info
        """
        if not self.is_trained:
            raise Exception("Model is not trained. Call train_model() first.")

        try:
            # Extract and validate input data
            ram = float(phone_specs.get("RAM"))
            storage = float(phone_specs.get("Storage"))
            display_size = float(phone_specs.get("Display Size"))
            battery = float(phone_specs.get("Battery Capacity"))
            quick_charge = int(phone_specs.get("Quick Charge"))
            ppi = int(phone_specs.get("Pixel Density"))
            os_type = phone_specs.get("Operating System")
            display_type = phone_specs.get("Display Technology")
            camera = float(phone_specs.get("camera"))
            chipset = int(phone_specs.get("CPU Manufacturing"))

            # Encode categorical variables
            os_encoded = self.safe_map(os_type, self.os_hierarchy)
            display_type_encoded = self.safe_map(
                display_type, self.display_type_hierarchy
            )

            # Create prediction dataframe
            new_data = pd.DataFrame(
                [
                    {
                        "RAM": ram,
                        "Storage": storage,
                        "Display Size": display_size,
                        "Battery Capacity": battery,
                        "Quick Charge": quick_charge,
                        "Pixel Density": ppi,
                        "os_encoded": os_encoded,
                        "display_type_encoded": display_type_encoded,
                        "camera": camera,
                        "CPU Manufacturing": chipset,
                    }
                ]
            )

            # Make prediction
            prediction_price = self.model.predict(new_data)[0]

            # Get feature importance
            feature_importance = dict(
                zip(self.feature_columns, self.model.feature_importances_)
            )
            top_features = sorted(
                feature_importance.items(), key=lambda x: x[1], reverse=True
            )[:10]

            # Find closest product
            closest_product = self._find_closest_product(prediction_price)

            return {
                "message": "XGBoost prediction successful",
                "price": round(prediction_price, 2),
                "encodings": {
                    "os": os_encoded,
                    "display_type": display_type_encoded,
                },
                "model_info": {
                    "algorithm": "XGBoost",
                    "top_features": [
                        {"feature": feat, "importance": round(imp, 4)}
                        for feat, imp in top_features
                    ],
                },
                "closest_product": closest_product,
            }

        except Exception as e:
            raise Exception(f"Prediction error: {str(e)}")

    def _find_closest_product(self, predicted_price):
        """Find the closest product by price"""
        if self.df is None:
            return "No data available"

        self.df["price_diff"] = (self.df["price"] - predicted_price).abs()
        closest_product = self.df.loc[self.df["price_diff"].idxmin()]
        return closest_product["Model"]

    def save_model(self, filepath):
        """Save the trained model to disk"""
        if not self.is_trained:
            raise Exception("Model is not trained yet")

        model_data = {
            "model": self.model,
            "scaler": self.scaler,
            "feature_columns": self.feature_columns,
            "os_hierarchy": self.os_hierarchy,
            "display_type_hierarchy": self.display_type_hierarchy,
        }
        joblib.dump(model_data, filepath)
        print(f"Model saved to {filepath}")

    def load_model(self, filepath):
        """Load a trained model from disk"""
        if not os.path.exists(filepath):
            raise Exception(f"Model file not found: {filepath}")

        model_data = joblib.load(filepath)
        self.model = model_data["model"]
        self.scaler = model_data["scaler"]
        self.feature_columns = model_data["feature_columns"]
        self.os_hierarchy = model_data["os_hierarchy"]
        self.display_type_hierarchy = model_data["display_type_hierarchy"]
        self.is_trained = True
        print(f"Model loaded from {filepath}")

    def get_model_info(self):
        """Get information about the model"""
        if not self.is_trained:
            return {"status": "Model not trained"}

        return {
            "status": "Model trained",
            "algorithm": "XGBoost Regressor",
            "features": self.feature_columns,
            "os_categories": list(self.os_hierarchy.keys()),
            "display_categories": list(self.display_type_hierarchy.keys()),
        }


# Example usage
if __name__ == "__main__":
    # Initialize model
    model = PhonePricePredictionModel(csv_path=r"C:\Users\pc\Desktop\AIbazaar\AIBazaar\AI\utils\notebooks\product_specs_en.csv")

    # Train model
    print("Training model...")
    training_results = model.train_model()
    print(f"Training completed: {training_results}")

    # Example prediction
    phone_specs = {
        "RAM": 8.0,
        "Storage": 128.0,
        "Display Size": 6.1,
        "Battery Capacity": 4000.0,
        "Quick Charge": 1,
        "Pixel Density": 400,
        "Operating System": "Android",
        "Display Technology": "AMOLED",
        "camera": 48.0,
        "CPU Manufacturing": 7,
    }

    try:
        result = model.predict_price(phone_specs)
        print(f"Prediction result: {result}")
    except Exception as e:
        print(f"Prediction error: {e}")

    # Save model
    model.save_model("phone_price_model.pkl")
