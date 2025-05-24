using Backend.Data.Context;
using Backend.Data.Entities;
using Backend.Dtos;
using Backend.Repositories.Abstract;

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

        public List<ProductDto> GetAllProducts()
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

        public Product GetProductById(int id)
        {
            return _context.Products.FirstOrDefault(p => p.ProductID == id);
        }
        public void AddProduct(Product product)
        {
            _context.Products.Add(product);
            _context.SaveChanges();
        }
        public void UpdateProduct(Product product)
        {
            _context.Products.Update(product);
            _context.SaveChanges();
        }
        public void DeleteProduct(int id)
        {
            var product = GetProductById(id);
            if (product != null)
            {
                _context.Products.Remove(product);
                _context.SaveChanges();
            }
        }
    }
}
