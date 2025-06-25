﻿using Backend.Dtos;
using Backend.Services;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;

namespace Backend.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class AuthController : ControllerBase
    {
        private readonly IConfiguration _configuration;

        private readonly AuthService _authService;

        public AuthController(IConfiguration configuration, AuthService authService)
        {
            _configuration = configuration;
            _authService = authService;
        }


        [HttpPost("register")]
        public IActionResult Register([FromBody] UserDto dto)
        {
            if (_authService.CheckEmailExists(dto.Email))
            {
                return BadRequest(new { Message = "Email already exists!" });
            }

            var user = _authService.Register(dto);
            var resultDto = new UserDto
            {
                FirstName = user.FirstName,
                LastName = user.LastName,
                Email = user.Email,
            };

            return Ok(resultDto);
        }

        [HttpPost("login")]
        public IActionResult Login([FromBody] LoginDto loginDto)
        {
            try
            {
                var token = _authService.Login(loginDto);
                return Ok(new {Token = token.AccessToken, Message = "Login successful." });

            }
            catch (Exception ex)
            {
                return BadRequest(new { Message = ex.Message, StackTrace = ex.StackTrace });
            }
        }

        [HttpGet("getIdFromToken")]
        public IActionResult getInfo(string t)
        {

            string userID = _authService.GetUserIdFromToken(t, _configuration);

            return Ok(new { User = userID, Message = "ID retrived from token" });

        }

        [HttpGet("getUserFromId")]
        public IActionResult getUserFromId(string id)
        {

            var user = _authService.getUserFromId(id, _configuration);
            if (user == null)
            {
                return NotFound("User not found");
            }
            user.Password = null;
            return Ok(user);
        }

        [HttpGet("getUserFromToken")]
        public IActionResult getUserFromToken([FromHeader(Name = "Authorization")] string jwt)
        {
            if (jwt == null)
            {
                return BadRequest("Missing token");
            }
            string token = jwt.Split(" ")[1];
            var user = _authService.getUserFromToken(token, _configuration);
            if (user == null)
            {
                return NotFound("User not found");
            }
            user.Password = null;
            return Ok(user);
        }
    }
}
