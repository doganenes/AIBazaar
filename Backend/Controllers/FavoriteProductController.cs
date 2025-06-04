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
        public IActionResult GetAllFavoriteProducts([FromQuery] string id)
        {
            var favoriteProducts = _favoriteProductService.GetFavoriteProductsByUserId(id);
            return Ok(favoriteProducts);
        }

        [HttpPost("addFavoriteProduct")]
        public IActionResult AddFavoriteProduct([FromBody] FavoriteProductRequestDto request)
        {
            try
            {
                bool added = _favoriteProductService.AddFavoriteProduct(request.UserId, request.ProductId);
                if (!added)
                    return BadRequest("This product is already in favorites.");

                return Ok("Product added to favorites.");
            }
            catch (KeyNotFoundException ex)
            {
                return NotFound(ex.Message);
            }
            catch (Exception ex)
            {
                return StatusCode(500, "An error occurred while adding the product.");
            }
        }


        [HttpDelete("removeFavoriteProduct")]
        public IActionResult RemoveFavoriteProduct(FavoriteProductRequestDto dto)
        {
            try
            {
                _favoriteProductService.RemoveFavoriteProduct(dto.UserId, dto.ProductId);
                return Ok("Product removed from favorites.");
            }
            catch (KeyNotFoundException ex)
            {
                return NotFound(ex.Message);
            }
            catch (Exception ex)
            {
                return StatusCode(500, "An error occurred while removing the product.");
            }
        }
    }
}