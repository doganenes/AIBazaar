import os

base_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(base_dir)
default_model_path = os.path.join(
            parent_dir, "models", "phone_price_model_20250630_225022.pkl"
        )

print(default_model_path)
