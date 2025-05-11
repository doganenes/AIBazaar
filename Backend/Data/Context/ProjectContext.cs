using Backend.Data.Entities;
using Microsoft.EntityFrameworkCore;

namespace Backend.Data.Context
{
    public class ProjectContext : DbContext
    {
        public ProjectContext(DbContextOptions<ProjectContext> options) : base(options)
        {
        }
        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<User>()
                .HasMany(u => u.FavoriteProducts)
                .WithMany(fp => fp.Users)
                .UsingEntity<Dictionary<string, object>>(
                    "FavoriteProductUser",
                    j => j
                        .HasOne<FavoriteProduct>()
                        .WithMany()
                        .HasForeignKey("FavoriteProductId")
                        .HasConstraintName("FK_FavoriteProductUser_FavoriteProducts_FavoriteProductId")
                        .OnDelete(DeleteBehavior.Cascade),
                    j => j
                        .HasOne<User>()
                        .WithMany()
                        .HasForeignKey("UserId")
                        .HasConstraintName("FK_FavoriteProductUser_Users_UserId")
                        .OnDelete(DeleteBehavior.Cascade));
        }

        public DbSet<User> Users { get; set; }
        public DbSet<FavoriteProduct> FavoriteProducts { get; set; }
        public DbSet<Product> Products { get; set; }
    }
}
