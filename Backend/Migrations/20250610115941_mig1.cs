using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace Backend.Migrations
{
    /// <inheritdoc />
    public partial class mig1 : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "LSTMProducts",
                columns: table => new
                {
                    ProductID = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    ProductName = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    Description = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    ImageUrl = table.Column<string>(type: "nvarchar(max)", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_LSTMProducts", x => x.ProductID);
                });

            migrationBuilder.CreateTable(
                name: "Users",
                columns: table => new
                {
                    UserId = table.Column<string>(type: "nvarchar(450)", nullable: false),
                    FirstName = table.Column<string>(type: "nvarchar(max)", nullable: true),
                    LastName = table.Column<string>(type: "nvarchar(max)", nullable: true),
                    Email = table.Column<string>(type: "nvarchar(max)", nullable: true),
                    Password = table.Column<string>(type: "nvarchar(max)", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Users", x => x.UserId);
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

            migrationBuilder.CreateTable(
                name: "LSTMProductPriceHistories",
                columns: table => new
                {
                    PriceHistoryID = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    ProductID = table.Column<int>(type: "int", nullable: false),
                    LSTMProductProductID = table.Column<int>(type: "int", nullable: false),
                    RecordDate = table.Column<DateTime>(type: "datetime2", nullable: false),
                    Price = table.Column<decimal>(type: "decimal(18,2)", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_LSTMProductPriceHistories", x => x.PriceHistoryID);
                    table.ForeignKey(
                        name: "FK_LSTMProductPriceHistories_LSTMProducts_LSTMProductProductID",
                        column: x => x.LSTMProductProductID,
                        principalTable: "LSTMProducts",
                        principalColumn: "ProductID",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "FavoriteProducts",
                columns: table => new
                {
                    FavoriteProductID = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    FavoriteProductDate = table.Column<DateTime>(type: "datetime2", nullable: false),
                    ProductID = table.Column<int>(type: "int", nullable: false),
                    UserId = table.Column<string>(type: "nvarchar(450)", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_FavoriteProducts", x => x.FavoriteProductID);
                    table.ForeignKey(
                        name: "FK_FavoriteProducts_LSTMProducts_ProductID",
                        column: x => x.ProductID,
                        principalTable: "LSTMProducts",
                        principalColumn: "ProductID",
                        onDelete: ReferentialAction.Cascade);
                    table.ForeignKey(
                        name: "FK_FavoriteProducts_Users_UserId",
                        column: x => x.UserId,
                        principalTable: "Users",
                        principalColumn: "UserId",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateIndex(
                name: "IX_FavoriteProducts_ProductID",
                table: "FavoriteProducts",
                column: "ProductID");

            migrationBuilder.CreateIndex(
                name: "IX_FavoriteProducts_UserId",
                table: "FavoriteProducts",
                column: "UserId");

            migrationBuilder.CreateIndex(
                name: "IX_LSTMProductPriceHistories_LSTMProductProductID",
                table: "LSTMProductPriceHistories",
                column: "LSTMProductProductID");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "FavoriteProducts");

            migrationBuilder.DropTable(
                name: "LSTMProductPriceHistories");

            migrationBuilder.DropTable(
                name: "XGBoostProducts");

            migrationBuilder.DropTable(
                name: "Users");

            migrationBuilder.DropTable(
                name: "LSTMProducts");
        }
    }
}
