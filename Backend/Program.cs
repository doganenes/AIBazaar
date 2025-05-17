using Backend.Data.Context;
using Backend.Data.Entities;
using Backend.Repositories.Abstract;
using Backend.Repositories.Concrete;
using Backend.Services;
using DotNetEnv;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.EntityFrameworkCore;
using Microsoft.IdentityModel.Tokens;
using System.Text;

var builder = WebApplication.CreateBuilder(args);

Env.Load();
var envConnectionString = Environment.GetEnvironmentVariable("DB_CONNECTION_STRING");
Console.WriteLine("Connection string: " + envConnectionString);

builder.Services.AddDbContext<ProjectContext>(options =>
    options.UseSqlServer("Server=DESKTOP-62B01VU\\SQLEXPRESS;Database=BazaarDb;Integrated Security=True;TrustServerCertificate=True"));

builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme).AddJwtBearer(opt =>
{
    opt.TokenValidationParameters = new Microsoft.IdentityModel.Tokens.TokenValidationParameters
    {
        ValidateAudience = true,
        ValidateIssuer = true,
        ValidateLifetime = true,
        ValidateIssuerSigningKey = true,
        ValidIssuer = builder.Configuration["Token:Issuer"],
        ValidAudience = builder.Configuration["Token:Audience"],
        IssuerSigningKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(builder.Configuration["Token:SecurityKey"])),
        ClockSkew = TimeSpan.Zero
    };
});

builder.Services.AddScoped(typeof(IRepository<User>), typeof(Repository<User>));
builder.Services.AddScoped(typeof(IRepository<Product>), typeof(Repository<Product>));
builder.Services.AddScoped(typeof(IRepository<FavoriteProduct>), typeof(Repository<FavoriteProduct>));

builder.Services.AddScoped<AuthService>();
builder.Services.AddScoped<FavoriteProductService>();
builder.Services.AddScoped<ProductService>();
builder.Services.AddControllers();
// Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowAll",
        builder => builder.AllowAnyOrigin()
                          .AllowAnyMethod()
                          .AllowAnyHeader());
});


var app = builder.Build();
// Configure the HTTP request pipeline.

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();

app.UseCors("AllowAll");
app.UseAuthorization();

app.MapControllers();
app.Run();

