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
            migrationBuilder.CreateTable(
                name: "KNN_Products",
                columns: table => new
                {
                    ProductId = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    ProductName = table.Column<string>(type: "nvarchar(max)", nullable: false),
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
                    table.PrimaryKey("PK_KNN_Products", x => x.ProductId);
                });
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "KNN_Products");
        }
    }
}
