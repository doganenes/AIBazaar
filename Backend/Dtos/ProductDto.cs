namespace Backend.Dtos
{
    public class ProductDto
    {
        public string ProductName { get; set; }
        public DateTime SaleDate { get; set; }
        public double Price { get; set; }
        public double Rating { get; set; }
        public string Description { get; set; }
        public string ImageUrl { get; set; }
        public bool IsInStock { get; set; }
    }
}
