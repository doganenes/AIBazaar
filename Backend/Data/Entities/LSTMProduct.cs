using System.ComponentModel.DataAnnotations;

namespace Backend.Data.Entities;
    public class LSTMProduct
    {
        [Key]
        public int LSTMProductID { get; set; }
        public int ProductID { get; set; }
        public string ProductName { get; set; }
        public DateTime SaleDate { get; set; }
        public double Price { get; set; }
        public string Description { get; set; }
        public string ImageUrl { get; set; }
        public ICollection<FavoriteProduct> FavoriteProducts { get; set; } = new List<FavoriteProduct>();
    }

