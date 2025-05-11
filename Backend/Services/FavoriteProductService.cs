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

        public void AddFavoriteProduct(string userId,int favoriteProductId)
        {
            var user = _projectContext.Users
               .Include(u => u.FavoriteProducts)
               .FirstOrDefault(u => u.UserId == userId);

            var favoriteProduct = _projectContext.FavoriteProducts
                .Include(b => b.Users)
                .FirstOrDefault(b => b.FavoriteProductID == favoriteProductId);

            if (user == null)
            {
                throw new KeyNotFoundException("User not found.");
            }

            if (favoriteProduct == null)
            {
                throw new KeyNotFoundException("Favorite product not found.");
            }

            favoriteProduct.Users.Add(user);
            user.FavoriteProducts.Add(favoriteProduct);
            _projectContext.SaveChanges();
        }

        public void RemoveFavoriteProduct(string userId, int favoriteProductId)
        {
            var user = _projectContext.Users
               .Include(u => u.FavoriteProducts)
               .FirstOrDefault(u => u.UserId == userId);
            var favoriteProduct = user.FavoriteProducts.FirstOrDefault(b => b.ProductID == favoriteProductId);

            if(user == null)
            {
                throw new InvalidOperationException("User not found!");

            }

            if (favoriteProduct == null)
            {
                throw new InvalidOperationException("Favorite product not found!");

            }

            user.FavoriteProducts.Remove(favoriteProduct);
            _projectContext.SaveChanges();
        }


        public List<ProductDto> GetFavoriteProductsByUserId(string userId)
        {
            var user = _projectContext.Users
                   .Include(u => u.FavoriteProducts)
                   .FirstOrDefault(u => u.UserId == userId);
            var favoriteProduct = user.FavoriteProducts?.Select(fp => new ProductDto
            {
                ProductName = fp.Product.ProductName,
                SaleDate = fp.Product.SaleDate,
                Price = fp.Product.Price,
                Rating = fp.Product.Rating,
                Description = fp.Product.Description,
                ImageUrl = fp.Product.ImageUrl,
                IsInStock = fp.Product.IsInStock

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

        public List<FavoriteProduct> GetAllFavoriteProducts()
        {
            return _favoriteProductRepository.GetAll().ToList();
        }

    }
}
