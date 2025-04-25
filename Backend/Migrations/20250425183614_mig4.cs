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
                name: "FK_FavoriteProductUser_FavoriteProducts_FavoriteProductsFavoriteProductID",
                table: "FavoriteProductUser");

            migrationBuilder.DropForeignKey(
                name: "FK_FavoriteProductUser_Users_UsersUserId",
                table: "FavoriteProductUser");

            migrationBuilder.RenameColumn(
                name: "UsersUserId",
                table: "FavoriteProductUser",
                newName: "UserId");

            migrationBuilder.RenameColumn(
                name: "FavoriteProductsFavoriteProductID",
                table: "FavoriteProductUser",
                newName: "FavoriteProductId");

            migrationBuilder.RenameIndex(
                name: "IX_FavoriteProductUser_UsersUserId",
                table: "FavoriteProductUser",
                newName: "IX_FavoriteProductUser_UserId");

            migrationBuilder.AddForeignKey(
                name: "FK_FavoriteProductUser_FavoriteProducts_FavoriteProductId",
                table: "FavoriteProductUser",
                column: "FavoriteProductId",
                principalTable: "FavoriteProducts",
                principalColumn: "FavoriteProductID",
                onDelete: ReferentialAction.Cascade);

            migrationBuilder.AddForeignKey(
                name: "FK_FavoriteProductUser_Users_UserId",
                table: "FavoriteProductUser",
                column: "UserId",
                principalTable: "Users",
                principalColumn: "UserId",
                onDelete: ReferentialAction.Cascade);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_FavoriteProductUser_FavoriteProducts_FavoriteProductId",
                table: "FavoriteProductUser");

            migrationBuilder.DropForeignKey(
                name: "FK_FavoriteProductUser_Users_UserId",
                table: "FavoriteProductUser");

            migrationBuilder.RenameColumn(
                name: "UserId",
                table: "FavoriteProductUser",
                newName: "UsersUserId");

            migrationBuilder.RenameColumn(
                name: "FavoriteProductId",
                table: "FavoriteProductUser",
                newName: "FavoriteProductsFavoriteProductID");

            migrationBuilder.RenameIndex(
                name: "IX_FavoriteProductUser_UserId",
                table: "FavoriteProductUser",
                newName: "IX_FavoriteProductUser_UsersUserId");

            migrationBuilder.AddForeignKey(
                name: "FK_FavoriteProductUser_FavoriteProducts_FavoriteProductsFavoriteProductID",
                table: "FavoriteProductUser",
                column: "FavoriteProductsFavoriteProductID",
                principalTable: "FavoriteProducts",
                principalColumn: "FavoriteProductID",
                onDelete: ReferentialAction.Cascade);

            migrationBuilder.AddForeignKey(
                name: "FK_FavoriteProductUser_Users_UsersUserId",
                table: "FavoriteProductUser",
                column: "UsersUserId",
                principalTable: "Users",
                principalColumn: "UserId",
                onDelete: ReferentialAction.Cascade);
        }
    }
}
