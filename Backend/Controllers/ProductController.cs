using Backend.Services;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;

namespace Backend.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class ProductController : ControllerBase
    {
        private readonly ProductService _productService;

        public ProductController(ProductService productService)
        {
            _productService = productService;
        }

        [HttpGet("getAllProducts")]
        public IActionResult GetAllProducts()
        {
           var values = _productService.GetAllProducts();
            return Ok(values);
        }

        [HttpGet("getProductById/{id}")]
        public IActionResult GetProductById(int id)
        {
            var value = _productService.GetProductById(id);
            if (value == null)
            {
                return NotFound();
            }
            return Ok(value);
        }
    }
}
