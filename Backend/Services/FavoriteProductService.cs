using Backend.Data.Context;
using Backend.Data.Entities;
using Backend.Dtos;
using Backend.Repositories.Abstract;
using Microsoft.EntityFrameworkCore;

namespace Backend.Services
{
    public class FavoriteProductService
    {
        private readonly IRepository<FavoriteProduct> _favoriteProductRepository;
        private readonly AuthService _authService;
        private readonly ProjectContext _projectContext;


        public FavoriteProductService(IRepository<FavoriteProduct> favoriteProductRepository, AuthService authService, ProjectContext projectContext)
        {
            _favoriteProductRepository = favoriteProductRepository;
            _authService = authService;
            _projectContext = projectContext;
        }

        public async Task AddFavoriteProductAsync(string userId, int productId)
        {
            var user = await _projectContext.Users
                .Include(u => u.FavoriteProducts)
                .FirstOrDefaultAsync(u => u.UserId == userId)
                ?? throw new KeyNotFoundException("User not found.");

            var product = await _projectContext.Products
                .Include(p => p.FavoriteProducts)
                .FirstOrDefaultAsync(p => p.ProductID == productId)
                ?? throw new KeyNotFoundException("Product not found.");

            bool alreadyFavorite = user.FavoriteProducts.Any(f => f.ProductID == productId);
            if (alreadyFavorite)
                throw new InvalidOperationException("This product is already in the user's favorites.");

            user.FavoriteProducts.Add(new FavoriteProduct
            {
                FavoriteProductDate = DateTime.Now,
                PriceChanging = 0,
                ProductID = productId,
                UserId = userId,
                Product = product,
                User = user
            });

            await _projectContext.SaveChangesAsync();
        }

        public async Task RemoveFavoriteProductAsync(string userId, int favoriteProductId)
        {
            var user = await _projectContext.Users
                .Include(u => u.FavoriteProducts)
                .FirstOrDefaultAsync(u => u.UserId == userId);

            if (user == null) return;

            var favoriteProduct = user.FavoriteProducts.FirstOrDefault(b => b.ProductID == favoriteProductId);

            if (favoriteProduct == null) return;

            user.FavoriteProducts.Remove(favoriteProduct);
            await _projectContext.SaveChangesAsync();
        }

        public async Task <List<FavoriteProductDto>> GetFavoriteProductsByUserId(string userId)
        {
            var user = _projectContext.Users
    .Include(u => u.FavoriteProducts)
        .ThenInclude(fp => fp.Product)
    .FirstOrDefault(u => u.UserId == userId);


            var favoriteProduct = user.FavoriteProducts?.Select(fp => new FavoriteProductDto
            {
                FavoriteProductID = fp.FavoriteProductID,
                FavoriteProductDate = fp.FavoriteProductDate,
                PriceChanging = fp.PriceChanging,
                Product = new ProductDto
                {
                    ProductID = fp.Product.ProductID,
                    ProductName = fp.Product.ProductName,
                    Price = fp.Product.Price,
                    Description = fp.Product.Description,
                    ImageUrl = fp.Product.ImageUrl
                }
            }).ToList();

            if (user == null)
            {
                throw new KeyNotFoundException("User not found.");
            }
            if (favoriteProduct == null)
            {
                throw new KeyNotFoundException("Favorite product not found.");
            }
            return favoriteProduct;
        }
    }
}
