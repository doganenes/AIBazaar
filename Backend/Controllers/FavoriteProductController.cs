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
        public async Task <IActionResult> GetAllFavoriteProducts([FromQuery] string id)
        {
            var favoriteProducts = await _favoriteProductService.GetFavoriteProductsByUserId(id);
            return Ok(favoriteProducts);
        }

        [HttpPost("addFavoriteProduct")]
        public async Task<IActionResult> AddFavoriteProduct([FromBody] FavoriteProductRequestDto request)
        {
            try
            {
                await _favoriteProductService.AddFavoriteProductAsync(request.UserId, request.ProductId);
                return Ok("Product added to favorites.");
            }
            catch (KeyNotFoundException ex)
            {
                return NotFound(ex.Message);
            }

            catch (InvalidOperationException ex)
            {
                return BadRequest(new { Error = ex.Message });
            }

            catch (Exception ex)
            {
                return StatusCode(500, "An error occurred while adding the product.");
            }
        }

        [HttpDelete("removeFavoriteProduct")]
        public async Task<IActionResult> RemoveFavoriteProduct(FavoriteProductRequestDto dto)
        {
            try
            {
                await _favoriteProductService.RemoveFavoriteProductAsync(dto.UserId, dto.ProductId);
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