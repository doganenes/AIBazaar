import React from 'react';

function Forecast() {
  return (
    <div className="container my-5">
      <div className="row justify-content-center g-4">
        <div className="col-12 col-md-5 mb-4 bg-secondary p-3 rounded me-md-4">
          <form>
            <h3 className='text-light'>Price estimate for a known phone </h3>
            <div className="mb-3">
              <label htmlFor="email1" className="form-label">Email address</label>
              <input type="email" className="form-control" id="email1" aria-describedby="emailHelp1" />
              <div id="emailHelp1" className="form-text">We'll never share your email with anyone else.</div>
            </div>
            <div className="mb-3">
              <label htmlFor="email1" className="form-label">Email address</label>
              <input type="email" className="form-control" id="email1" aria-describedby="emailHelp1" />
              <div id="emailHelp1" className="form-text">We'll never share your email with anyone else.</div>
            </div>
            <div className="mb-3">
              <label htmlFor="email1" className="form-label">Email address</label>
              <input type="email" className="form-control" id="email1" aria-describedby="emailHelp1" />
              <div id="emailHelp1" className="form-text">We'll never share your email with anyone else.</div>
            </div>
            <div className="mb-3">
              <label htmlFor="email1" className="form-label">Email address</label>
              <input type="email" className="form-control" id="email1" aria-describedby="emailHelp1" />
              <div id="emailHelp1" className="form-text">We'll never share your email with anyone else.</div>
            </div>
            <div className="mb-3">
              <label htmlFor="email1" className="form-label">Email address</label>
              <input type="email" className="form-control" id="email1" aria-describedby="emailHelp1" />
              <div id="emailHelp1" className="form-text">We'll never share your email with anyone else.</div>
            </div>
            <button type="submit" className="btn btn-primary">Submit</button>
          </form>
        </div>

        <div className="col-12 col-md-5 mb-4 p-3 bg-secondary rounded ms-md-4">
          <form>
            <h3 className='text-light'>Price estimate for features </h3>
            <div className="mb-3">
              <label htmlFor="email2" className="form-label">Email address</label>
              <input type="email" className="form-control" id="email2" aria-describedby="emailHelp2" />
              <div id="emailHelp2" className="form-text">We'll never share your email with anyone else.</div>
            </div>
 
            <div className="mb-3">
              <label htmlFor="email2" className="form-label">Email address</label>
              <input type="email" className="form-control" id="email2" aria-describedby="emailHelp2" />
              <div id="emailHelp2" className="form-text">We'll never share your email with anyone else.</div>
            </div>
 
            <div className="mb-3">
              <label htmlFor="email2" className="form-label">Email address</label>
              <input type="email" className="form-control" id="email2" aria-describedby="emailHelp2" />
              <div id="emailHelp2" className="form-text">We'll never share your email with anyone else.</div>
            </div>
 
            <div className="mb-3">
              <label htmlFor="email2" className="form-label">Email address</label>
              <input type="email" className="form-control" id="email2" aria-describedby="emailHelp2" />
              <div id="emailHelp2" className="form-text">We'll never share your email with anyone else.</div>
            </div>
 
            <div className="mb-3">
              <label htmlFor="email2" className="form-label">Email address</label>
              <input type="email" className="form-control" id="email2" aria-describedby="emailHelp2" />
              <div id="emailHelp2" className="form-text">We'll never share your email with anyone else.</div>
            </div>
            <button type="submit" className="btn btn-primary">Submit</button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default Forecast;