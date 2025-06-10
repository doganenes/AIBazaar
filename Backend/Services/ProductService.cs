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
        private readonly IRepository<LSTMProduct> _productRepository;
        public ProductService(ProjectContext context, IRepository<LSTMProduct> repository)
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
                Description = x.Description,
                ImageUrl = x.ImageUrl
            }).ToList();
        }

        public async Task<ProductDetailDto> GetProductById(int id)
        {
            return _context.LSTMProducts
                .Where(x => x.ProductID == id)
                .Select(x => new ProductDetailDto
                {
                    ProductName = x.ProductName,
                    Description = x.Description,
                    ImageUrl = x.ImageUrl
                })
                .FirstOrDefault();
        }

        public async Task<List<LSTMProduct>> SearchProductsAsync(SearchProductDto dto)
        {
            IQueryable<LSTMProduct> query = _context.LSTMProducts.AsQueryable();

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

            return await query.ToListAsync();
        }

    }
}
