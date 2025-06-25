using System.ComponentModel.DataAnnotations.Schema;
using System.ComponentModel.DataAnnotations;

namespace Backend.Data.Entities
{
    public class LSTMProductPriceHistory
    {
        [Key]
        public int PriceHistoryID { get; set; }

        [ForeignKey("LSTMProduct")]
        public int ProductID { get; set; }
        public LSTMProduct LSTMProduct { get; set; }
        public string? ProductName { get; set; }

        public DateTime? RecordDate { get; set; }
        public decimal? Price { get; set; }
    }
}
