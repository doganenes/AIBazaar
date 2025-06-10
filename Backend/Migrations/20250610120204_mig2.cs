using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace Backend.Migrations
{
    /// <inheritdoc />
    public partial class mig2 : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_LSTMProductPriceHistories_LSTMProducts_LSTMProductProductID",
                table: "LSTMProductPriceHistories");

            migrationBuilder.AlterColumn<int>(
                name: "LSTMProductProductID",
                table: "LSTMProductPriceHistories",
                type: "int",
                nullable: true,
                oldClrType: typeof(int),
                oldType: "int");

            migrationBuilder.AddForeignKey(
                name: "FK_LSTMProductPriceHistories_LSTMProducts_LSTMProductProductID",
                table: "LSTMProductPriceHistories",
                column: "LSTMProductProductID",
                principalTable: "LSTMProducts",
                principalColumn: "ProductID");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_LSTMProductPriceHistories_LSTMProducts_LSTMProductProductID",
                table: "LSTMProductPriceHistories");

            migrationBuilder.AlterColumn<int>(
                name: "LSTMProductProductID",
                table: "LSTMProductPriceHistories",
                type: "int",
                nullable: false,
                defaultValue: 0,
                oldClrType: typeof(int),
                oldType: "int",
                oldNullable: true);

            migrationBuilder.AddForeignKey(
                name: "FK_LSTMProductPriceHistories_LSTMProducts_LSTMProductProductID",
                table: "LSTMProductPriceHistories",
                column: "LSTMProductProductID",
                principalTable: "LSTMProducts",
                principalColumn: "ProductID",
                onDelete: ReferentialAction.Cascade);
        }
    }
}
