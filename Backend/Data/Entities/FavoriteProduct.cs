using Backend.Data.Entities;
using System.Collections.ObjectModel;

public class FavoriteProduct
{
    public int FavoriteProductID { get; set; }
    public DateTime FavoriteProductDate { get; set; }
    public short PriceChanging { get; set; }

    public int ProductID { get; set; }
    public Product Product { get; set; }

    public ICollection<User> Users { get; set; } = new Collection<User>();
}
