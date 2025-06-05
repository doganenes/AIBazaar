using Backend.Data.Context;
using Backend.Data.Entities;
using Backend.Dtos;
using Backend.Repositories.Abstract;
using Microsoft.EntityFrameworkCore;

namespace Backend.Services
{
    public class ProductService
    {
        private readonly ProjectContext _context;
        private readonly IRepository<Product> _productRepository;
        public ProductService(ProjectContext context, IRepository<Product> repository)
        {
            _context = context;
            _productRepository = repository;
        }

        public async Task<List<ProductDto>> GetAllProducts()
        {
            return _productRepository.GetAll().Select(x => new ProductDto
            {
                ProductID = x.ProductID,
                ProductName = x.ProductName,
                Price = x.Price,
                Description = x.Description,
                ImageUrl = x.ImageUrl
            }).ToList();
        }

        public async Task<ProductDetailDto> GetProductById(int id)
        {
            return _context.Products
                .Where(x => x.ProductID == id)
                .Select(x => new ProductDetailDto
                {
                    ProductName = x.ProductName,
                    Price = x.Price,
                    Description = x.Description,
                    ImageUrl = x.ImageUrl
                })
                .FirstOrDefault();
        }

        public async Task<List<Product>> SearchProductsAsync(SearchProductDto dto)
        {
            IQueryable<Product> query = _context.Products.AsQueryable();

            if (!string.IsNullOrWhiteSpace(dto.ProductName))
            {
                query = query.Where(p => p.ProductName.ToLower().Contains(dto.ProductName.ToLower()));
            }

            if (!string.IsNullOrWhiteSpace(dto.Description))
            {
                query = query.Where(p => p.Description.ToLower().Contains(dto.Description.ToLower()));
            }

            if (!string.IsNullOrWhiteSpace(dto.ImageUrl))
            {
                query = query.Where(p => p.ImageUrl.ToLower().Contains(dto.ImageUrl.ToLower()));
            }

            if (dto.Price.HasValue)
            {
                query = query.Where(p => p.Price == dto.Price.Value);
            }

            return await query.ToListAsync();
        }

    }
}
