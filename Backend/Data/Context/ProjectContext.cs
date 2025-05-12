using Backend.Data.Entities;
using Microsoft.EntityFrameworkCore;

namespace Backend.Data.Context
{
    public class ProjectContext : DbContext
    {
        public ProjectContext(DbContextOptions<ProjectContext> options) : base(options)
        {
        }

        public DbSet<User> Users { get; set; }
        public DbSet<FavoriteProduct> FavoriteProducts { get; set; }
        public DbSet<Product> Products { get; set; }
    }
}