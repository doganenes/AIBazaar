using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace Backend.Migrations
{
    /// <inheritdoc />
    public partial class mig3 : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_LSTMProductPriceHistories_LSTMProducts_LSTMProductProductID",
                table: "LSTMProductPriceHistories");

            migrationBuilder.DropIndex(
                name: "IX_LSTMProductPriceHistories_LSTMProductProductID",
                table: "LSTMProductPriceHistories");

            migrationBuilder.DropColumn(
                name: "LSTMProductProductID",
                table: "LSTMProductPriceHistories");

            migrationBuilder.CreateIndex(
                name: "IX_LSTMProductPriceHistories_ProductID",
                table: "LSTMProductPriceHistories",
                column: "ProductID");

            migrationBuilder.AddForeignKey(
                name: "FK_LSTMProductPriceHistories_LSTMProducts_ProductID",
                table: "LSTMProductPriceHistories",
                column: "ProductID",
                principalTable: "LSTMProducts",
                principalColumn: "ProductID",
                onDelete: ReferentialAction.Cascade);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_LSTMProductPriceHistories_LSTMProducts_ProductID",
                table: "LSTMProductPriceHistories");

            migrationBuilder.DropIndex(
                name: "IX_LSTMProductPriceHistories_ProductID",
                table: "LSTMProductPriceHistories");

            migrationBuilder.AddColumn<int>(
                name: "LSTMProductProductID",
                table: "LSTMProductPriceHistories",
                type: "int",
                nullable: true);

            migrationBuilder.CreateIndex(
                name: "IX_LSTMProductPriceHistories_LSTMProductProductID",
                table: "LSTMProductPriceHistories",
                column: "LSTMProductProductID");

            migrationBuilder.AddForeignKey(
                name: "FK_LSTMProductPriceHistories_LSTMProducts_LSTMProductProductID",
                table: "LSTMProductPriceHistories",
                column: "LSTMProductProductID",
                principalTable: "LSTMProducts",
                principalColumn: "ProductID");
        }
    }
}
