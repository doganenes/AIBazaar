using System.Collections.ObjectModel;
namespace Backend.Data.Entities;
public class FavoriteProduct
{
    public int FavoriteProductID { get; set; }
    public DateTime FavoriteProductDate { get; set; }
    public short PriceChanging { get; set; }

    public int ProductID { get; set; }
    public Product Product { get; set; }

    public string UserId { get; set; }
    public User User { get; set; } 
}
<<<<<<< HEAD
    
=======

>>>>>>> 814fed5a2d8857a266a3ef065a6ee92198272dc3
