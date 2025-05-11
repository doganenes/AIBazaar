using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace Backend.Migrations
{
    /// <inheritdoc />
    public partial class mig5 : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "Popularity",
                table: "Products");

            migrationBuilder.AddColumn<int>(
                name: "ProductID",
                table: "Users",
                type: "int",
                nullable: true);

            migrationBuilder.CreateIndex(
                name: "IX_Users_ProductID",
                table: "Users",
                column: "ProductID");

            migrationBuilder.CreateIndex(
                name: "IX_FavoriteProducts_ProductID",
                table: "FavoriteProducts",
                column: "ProductID");

            migrationBuilder.AddForeignKey(
                name: "FK_FavoriteProducts_Products_ProductID",
                table: "FavoriteProducts",
                column: "ProductID",
                principalTable: "Products",
                principalColumn: "ProductID",
                onDelete: ReferentialAction.Cascade);

            migrationBuilder.AddForeignKey(
                name: "FK_Users_Products_ProductID",
                table: "Users",
                column: "ProductID",
                principalTable: "Products",
                principalColumn: "ProductID");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_FavoriteProducts_Products_ProductID",
                table: "FavoriteProducts");

            migrationBuilder.DropForeignKey(
                name: "FK_Users_Products_ProductID",
                table: "Users");

            migrationBuilder.DropIndex(
                name: "IX_Users_ProductID",
                table: "Users");

            migrationBuilder.DropIndex(
                name: "IX_FavoriteProducts_ProductID",
                table: "FavoriteProducts");

            migrationBuilder.DropColumn(
                name: "ProductID",
                table: "Users");

            migrationBuilder.AddColumn<short>(
                name: "Popularity",
                table: "Products",
                type: "smallint",
                nullable: false,
                defaultValue: (short)0);
        }
    }
}
