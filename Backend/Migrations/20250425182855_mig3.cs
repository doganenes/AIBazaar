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
                name: "FK_FavoriteProducts_Users_UserId",
                table: "FavoriteProducts");

            migrationBuilder.DropIndex(
                name: "IX_FavoriteProducts_UserId",
                table: "FavoriteProducts");

            migrationBuilder.DropColumn(
                name: "UserId",
                table: "FavoriteProducts");

            migrationBuilder.CreateTable(
                name: "FavoriteProductUser",
                columns: table => new
                {
                    FavoriteProductsFavoriteProductID = table.Column<int>(type: "int", nullable: false),
                    UsersUserId = table.Column<string>(type: "nvarchar(450)", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_FavoriteProductUser", x => new { x.FavoriteProductsFavoriteProductID, x.UsersUserId });
                    table.ForeignKey(
                        name: "FK_FavoriteProductUser_FavoriteProducts_FavoriteProductsFavoriteProductID",
                        column: x => x.FavoriteProductsFavoriteProductID,
                        principalTable: "FavoriteProducts",
                        principalColumn: "FavoriteProductID",
                        onDelete: ReferentialAction.Cascade);
                    table.ForeignKey(
                        name: "FK_FavoriteProductUser_Users_UsersUserId",
                        column: x => x.UsersUserId,
                        principalTable: "Users",
                        principalColumn: "UserId",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateIndex(
                name: "IX_FavoriteProductUser_UsersUserId",
                table: "FavoriteProductUser",
                column: "UsersUserId");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "FavoriteProductUser");

            migrationBuilder.AddColumn<string>(
                name: "UserId",
                table: "FavoriteProducts",
                type: "nvarchar(450)",
                nullable: true);

            migrationBuilder.CreateIndex(
                name: "IX_FavoriteProducts_UserId",
                table: "FavoriteProducts",
                column: "UserId");

            migrationBuilder.AddForeignKey(
                name: "FK_FavoriteProducts_Users_UserId",
                table: "FavoriteProducts",
                column: "UserId",
                principalTable: "Users",
                principalColumn: "UserId");
        }
    }
}
