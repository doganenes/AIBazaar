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

        public bool AddFavoriteProduct(string userId, int productId)
        {
            var user = _projectContext.Users
               .Include(u => u.FavoriteProducts)
               .FirstOrDefault(u => u.UserId == userId);

            var product = _projectContext.Products
                .Include(p => p.FavoriteProducts)
                .FirstOrDefault(p => p.ProductID == productId);

            if (user == null)
                throw new KeyNotFoundException("User not found.");

            if (product == null)
                throw new KeyNotFoundException("Product not found.");

            bool alreadyFavorite = user.FavoriteProducts
                .Any(f => f.ProductID == productId);

            if (alreadyFavorite)
                return false; 

            user.FavoriteProducts.Add(new FavoriteProduct
            {
                FavoriteProductDate = DateTime.Now,
                PriceChanging = 0,
                ProductID = productId,
                UserId = userId,
                Product = product,
                User = user
            });

            _projectContext.SaveChanges();
            return true;
        }


        public void RemoveFavoriteProduct(string userId, int favoriteProductId)
        {
            var user = _projectContext.Users
               .Include(u => u.FavoriteProducts)
               .FirstOrDefault(u => u.UserId == userId);
            var favoriteProduct = user.FavoriteProducts.FirstOrDefault(b => b.ProductID == favoriteProductId);

            user.FavoriteProducts.Remove(favoriteProduct);
            _projectContext.SaveChanges();
        }


        public List<FavoriteProductDto> GetFavoriteProductsByUserId(string userId)
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
