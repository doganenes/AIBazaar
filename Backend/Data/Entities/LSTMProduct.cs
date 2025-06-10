using System.ComponentModel.DataAnnotations;

namespace Backend.Data.Entities;
    public class LSTMProduct
    {
    [Key]
    public int ProductID { get; set; }
    public string ProductName { get; set; }
    public string Description { get; set; }
    public string ImageUrl { get; set; }

    public ICollection<FavoriteProduct> FavoriteProducts { get; set; } = new List<FavoriteProduct>();
    public ICollection<LSTMProductPriceHistory> PriceHistory { get; set; } = new List<LSTMProductPriceHistory>();
    }

