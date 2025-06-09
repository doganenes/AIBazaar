using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace Backend.Migrations
{
    /// <inheritdoc />
    public partial class mig4 : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_FavoriteProducts_Products_ProductID",
                table: "FavoriteProducts");

            migrationBuilder.DropTable(
                name: "KNN_Products");

            migrationBuilder.DropTable(
                name: "Products");

            migrationBuilder.CreateTable(
                name: "LSTMProducts",
                columns: table => new
                {
                    LSTMProductID = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    ProductID = table.Column<int>(type: "int", nullable: false),
                    ProductName = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    SaleDate = table.Column<DateTime>(type: "datetime2", nullable: false),
                    Price = table.Column<double>(type: "float", nullable: false),
                    Description = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    ImageUrl = table.Column<string>(type: "nvarchar(max)", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_LSTMProducts", x => x.LSTMProductID);
                });

            migrationBuilder.CreateTable(
                name: "XGBoostProducts",
                columns: table => new
                {
                    ProductId = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    Storage = table.Column<int>(type: "int", nullable: false),
                    RAM = table.Column<int>(type: "int", nullable: false),
                    OS = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    PPI = table.Column<int>(type: "int", nullable: false),
                    Battery = table.Column<int>(type: "int", nullable: false),
                    Foldable = table.Column<bool>(type: "bit", nullable: false),
                    Display_Type = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    CPU_Core = table.Column<int>(type: "int", nullable: false),
                    Video_Resolution = table.Column<string>(type: "nvarchar(max)", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_XGBoostProducts", x => x.ProductId);
                });

            migrationBuilder.AddForeignKey(
                name: "FK_FavoriteProducts_LSTMProducts_ProductID",
                table: "FavoriteProducts",
                column: "ProductID",
                principalTable: "LSTMProducts",
                principalColumn: "LSTMProductID",
                onDelete: ReferentialAction.Cascade);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_FavoriteProducts_LSTMProducts_ProductID",
                table: "FavoriteProducts");

            migrationBuilder.DropTable(
                name: "LSTMProducts");

            migrationBuilder.DropTable(
                name: "XGBoostProducts");

            migrationBuilder.CreateTable(
                name: "KNN_Products",
                columns: table => new
                {
                    ProductId = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    Battery = table.Column<int>(type: "int", nullable: false),
                    CPU_Core = table.Column<int>(type: "int", nullable: false),
                    Display_Type = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    Foldable = table.Column<bool>(type: "bit", nullable: false),
                    OS = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    PPI = table.Column<int>(type: "int", nullable: false),
                    ProductName = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    RAM = table.Column<int>(type: "int", nullable: false),
                    Storage = table.Column<int>(type: "int", nullable: false),
                    Video_Resolution = table.Column<string>(type: "nvarchar(max)", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_KNN_Products", x => x.ProductId);
                });

            migrationBuilder.CreateTable(
                name: "Products",
                columns: table => new
                {
                    ProductID = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    Description = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    ImageUrl = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    Price = table.Column<double>(type: "float", nullable: false),
                    ProductName = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    SaleDate = table.Column<DateTime>(type: "datetime2", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Products", x => x.ProductID);
                });

            migrationBuilder.AddForeignKey(
                name: "FK_FavoriteProducts_Products_ProductID",
                table: "FavoriteProducts",
                column: "ProductID",
                principalTable: "Products",
                principalColumn: "ProductID",
                onDelete: ReferentialAction.Cascade);
        }
    }
}
