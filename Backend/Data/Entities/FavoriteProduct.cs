namespace Backend.Data.Entities
{
    public class FavoriteProduct
    {
        public int FavoriteProductID { get; set; }
        public DateTime FavoriteProductDate { get; set; }
        public short PriceChanging { get; set; }
        public int ProductID { get; set; }
    }
}
