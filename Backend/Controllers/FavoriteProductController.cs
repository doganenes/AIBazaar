using Backend.Data.Context;
using Backend.Dtos;
using Backend.Services;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;

namespace Backend.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class FavoriteProductController : ControllerBase
    {
        private readonly FavoriteProductService _favoriteProductService;
        
        public FavoriteProductController(FavoriteProductService favoriteProductService, AuthService authService, IConfiguration configuration, ProductService productService, ProjectContext projectContext)
        {
            _favoriteProductService = favoriteProductService;
        }

        [HttpGet("getAllFavoriteProducts")]
        public IActionResult GetAllFavoriteProducts()
        {
            var favoriteProducts = _favoriteProductService.GetAllFavoriteProducts();
            return Ok(favoriteProducts);
        }

        [HttpPost("addFavoriteProduct")]
        public IActionResult AddFavoriteProduct([FromQuery] string userId, int productId)
        {
            _favoriteProductService.AddFavoriteProduct(userId, productId);
            return Ok("Product added to favorites.");
        }

        [HttpDelete("removeFavoriteProduct")]
        public IActionResult RemoveFavoriteProduct([FromQuery] string userId, int productId)
        {
            _favoriteProductService.RemoveFavoriteProduct(userId, productId);
            return Ok("Product removed from favorites.");
        }

        [HttpGet("getFavoriteProductsByUserId")]
        public IActionResult GetFavoriteProductsByUserId([FromQuery] string userId)
        {
            var values = _favoriteProductService.GetFavoriteProductsByUserId(userId);
            return Ok(values);
        }
    }
}
