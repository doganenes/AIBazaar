﻿using System.Collections.ObjectModel;
namespace Backend.Data.Entities;
public class FavoriteProduct
{
    public int FavoriteProductID { get; set; }
    public DateTime FavoriteProductDate { get; set; }
    public int ProductID { get; set; }
    public LSTMProduct Product { get; set; }
    public string UserId { get; set; }
    public User User { get; set; } 
}