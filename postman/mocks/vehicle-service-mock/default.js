const http = require("http");

const vehicles = [
  {
    id: 1,
    nickName: "The Lisa Marie",
    vin: "4M2DV11W4RDJ53329",
    make: "Mercury",
    model: "Villager",
    year: "1994",
    miles: 159864
  },
  {
    id: 2,
    nickName: "Dolly",
    vin: "JN8AZ2KR1AT169594",
    make: "Nissan",
    model: "Cube",
    year: "2010",
    miles: 59000
  }
];

const server = http.createServer((req, res) => {
  const url = req.url;
  const method = req.method;

  // Parse body helper
  const parseBody = (callback) => {
    let body = "";
    req.on("data", (chunk) => { body += chunk.toString(); });
    req.on("end", () => {
      try { callback(JSON.parse(body)); }
      catch (e) { callback({}); }
    });
  };

  // GET /vehicles
  // @endpoint GET /vehicles
  if (method === "GET" && url === "/vehicles") {
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify([
      {
        id: 1,
        nickName: "The Lisa Marie",
        vin: "4M2DV11W4RDJ53329",
        make: "Mercury",
        model: "Villager",
        year: "1994",
        miles: 159864
      },
      {
        id: 2,
        nickName: "Dolly",
        vin: "JN8AZ2KR1AT169594",
        make: "Nissan",
        model: "Cube",
        year: "2010",
        miles: 59000
      }
    ]));
    return;
  }

  // POST /vehicles
  // @endpoint POST /vehicles
  if (method === "POST" && url === "/vehicles") {
    parseBody((body) => {
      const newVehicle = Object.assign({ id: 1 }, body);
      res.writeHead(201, { "Content-Type": "application/json" });
      res.end(JSON.stringify({
        id: 1,
        nickName: body.nickName || "The Lisa Marie",
        vin: body.vin || "4M2DV11W4RDJ53329",
        make: body.make || "Mercury",
        model: body.model || "Villager",
        year: body.year || "1994",
        miles: body.miles || "159,864"
      }));
    });
    return;
  }

  // Match /vehicles/:id
  const vehicleIdMatch = url.match(/^\/vehicles\/([^/?]+)(\?.*)?$/);

  // GET /vehicles/:id
  // @endpoint GET /vehicles/:id
  if (method === "GET" && vehicleIdMatch) {
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify({
      id: 1,
      nickName: "The Lisa Marie",
      vin: "4M2DV11W4RDJ53329",
      make: "Mercury",
      model: "Villager",
      year: "1994",
      miles: 159864
    }));
    return;
  }

  // PATCH /vehicles/:id
  // @endpoint PATCH /vehicles/:id
  if (method === "PATCH" && vehicleIdMatch) {
    parseBody((body) => {
      res.writeHead(200, { "Content-Type": "application/json" });
      res.end(JSON.stringify({
        id: 1,
        nickName: body.nickName || "The Lisa Marie",
        vin: body.vin || "4M2DV11W4RDJ53329",
        make: body.make || "Mercury",
        model: body.model || "Villager",
        year: body.year || "1994",
        miles: body.miles || 159999
      }));
    });
    return;
  }

  // DELETE /vehicles/:id
  // @endpoint DELETE /vehicles/:id
  if (method === "DELETE" && vehicleIdMatch) {
    res.writeHead(204, {});
    res.end("");
    return;
  }

  // 404 fallback
  res.writeHead(404, { "Content-Type": "application/json" });
  res.end(JSON.stringify({ error: "Not found" }));
});

server.listen(process.env.PORT || 4500);
