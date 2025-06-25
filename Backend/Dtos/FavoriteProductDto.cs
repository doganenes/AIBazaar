using Backend.Data.Entities;

namespace Backend.Dtos
{
    public class FavoriteProductDto
    {
        public int FavoriteProductID { get; set; }
        public DateTime FavoriteProductDate { get; set; }
        public ProductDto Product { get; set; }
    }

}