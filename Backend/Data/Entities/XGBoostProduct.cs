using System.ComponentModel.DataAnnotations;

namespace Backend.Data.Entities
{
    public class XGBoostProduct
    {
        [Key]
        public int ProductId { get; set; }
        public int Storage { get; set; }
        public int RAM { get; set; }
        public string OS { get; set; }
        public int PPI { get; set; }
        public int Battery { get; set; }
        public bool Foldable { get; set; }
        public string Display_Type { get; set; }
        public int CPU_Core { get; set; }
        public string Video_Resolution { get; set; }
        
    }
}
