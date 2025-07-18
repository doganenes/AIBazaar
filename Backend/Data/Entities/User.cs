﻿using System.Collections.ObjectModel;
using System.ComponentModel.DataAnnotations;
namespace Backend.Data.Entities;
    public class User
    {
        [Key]
        public string UserId { get; set; }
        public string? FirstName { get; set; }
        public string? LastName { get; set; }
        public string? Email { get; set; }
        public string? Password { get; set; }

        public ICollection<FavoriteProduct> FavoriteProducts { get; set; } = new Collection<FavoriteProduct>();
    }

