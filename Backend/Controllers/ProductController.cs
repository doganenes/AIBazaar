using Backend.Dtos;
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
        public async Task<IActionResult> GetAllProducts()
        {
            var values = await _productService.GetAllProducts();
            return Ok(values);
        }

        [HttpGet("getProductById/{id}")]
        public async Task<IActionResult> GetProductById(int id)
        {
            var value = await _productService.GetProductById(id);
            if (value == null)
            {
                return NotFound();
            }
            return Ok(value);
        }

        [HttpPost("searchProducts")]
        public async Task<IActionResult> SearchProducts([FromBody] SearchProductDto dto)
        {
            if (dto == null)
            {
                return BadRequest("Search criteria cannot be null.");
            }

            var products = await _productService.SearchProductsAsync(dto);
            return Ok(products);
        }
    }
}