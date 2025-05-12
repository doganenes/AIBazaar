import "./App.css";
import Home from "../pages/Home";
import Signin from "../pages/Signin";
import Signup from "../pages/Signup";
import NotFound from "../pages/NotFound";
import { Container } from "react-bootstrap";
import Header from "../components/Header";
import { Route, Routes } from "react-router-dom";
import Forecast from "../pages/Forecast";
import Favorites from "../pages/Favorites";

function App() {
  return (
    <div>
      <Container>
        <Header/>
        <Routes>
          <Route path="/" element={<Home />}></Route>
          <Route path="/home" element={<Home />}></Route>
          <Route path="/signup" element={<Signup />}></Route>
          <Route path="/signin" element={<Signin />}></Route>
          <Route path="/forecast" element={<Forecast/>}></Route>
          <Route path="/favorites" element={<Favorites/>}></Route>
          <Route path="*" element={<NotFound />}></Route>
      </Routes>
      </Container>
    </div>
  );
}

export default App;
