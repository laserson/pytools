streamgraph_html = r"""
<html>
    <head>
        <title>Visualization</title>
        <script type="text/javascript" src="../protovis-r3.2.js"></script>
    </head>

    <body>
        <script type="text/javascript+protovis">
            
            data = %s
            
            // Unpack data and sort it accordingly
            var times = data.times ;
            var sums = data.sums ;
            var matrix = data.matrix ;
            
            function first_nonzero_index(v) {
                for( i=0; i<v.length; i++) {
                    if(v[i] > 0) {
                        break;
                    }
                }
                return i;
            }
            
            // sort data according to first nonzero index in timeseries
            matrix.sort(function(a,b) (first_nonzero_index(a)-first_nonzero_index(b)))
            
            // Define some parameters for the visualization
            var frame_w = document.body.clientWidth,
                frame_h = document.body.clientHeight,
                vis_w = frame_w - 50
                vis_h = frame_h - 100
                x = pv.Scale.linear(pv.min(times), pv.max(times)).range(0, vis_w),
                y = pv.Scale.linear(0,1).range(0, vis_h);
            
            function norm_weight(v) {
                sum = 0;
                for( i=0; i<v.length; i++) {
                    sum += v[i] / sums[i];
                }
                return sum;
            }
            
            var min_norm_weight = pv.min(matrix.map(norm_weight)),
                max_norm_weight = pv.max(matrix.map(norm_weight));
            
            Hscale = pv.Scale.linear(pv.range(times.length)).range(0,360-360/times.length)
            Lscale = pv.Scale.root(min_norm_weight,max_norm_weight).range(80,50).power(4)
            function color_picker(d) {
                h = Hscale(first_nonzero_index(d))
                s = 100
                l = Lscale(norm_weight(d))
                return pv.color("hsl("+h+","+s+"%%,"+l+"%%)");
            }
            
            // Start the visualization
            var frame = new pv.Panel()
                .width(frame_w)
                .height(frame_h);
                // .strokeStyle("#000")
            
            vis = frame.add(pv.Panel)
                .width(vis_w)
                .height(vis_h)
                .left((frame_w - vis_w) / 2.0);
                // .strokeStyle("#000")
            
            vis.add(pv.Layout.Stack)
                .layers(matrix)
                // .order("inside-out")
                .offset("wiggle")
                .x(function() x(times[this.index]))
                .y(function(d) y(d/sums[this.index]))
              .layer.add(pv.Area)
                .fillStyle(function(d,p) color_picker(p));
                // .interpolate("basis")    // makes it pretty
            
            // Panel with time ticks
            vis.add(pv.Panel)
                .width(vis_w)
                .height(100)
                .left(0)
                .bottom(-100)    // Adjust here to move time ticks up/down
                // .strokeStyle("#000")
              .add(pv.Rule)
                .data(times)
                // .visible(function(d) d)
                .left(x)
                .bottom(25)
                .height(5)
              .anchor("bottom").add(pv.Label)
              .anchor("top").add(pv.Bar)
                  .bottom(function() (this.index==3)? 65 : 35)
                  .left(function(d) x(d)-8)
                  .height(20)
                  .width(16)
                  .fillStyle(function() pv.color("hsl("+Hscale(this.index)+",100%%,50%%)"));
            
            // vis.add(pv.Rule)
            //     .data(y.ticks())
            //     .bottom(y)
            //   .anchor('left').add(pv.Label)
            //     .text(y.tickFormat);
            
            frame.render();
    
            document.getElementById("svgoutput").value = vis.scene[0].canvas.innerHTML;
    
    
        </script>
        <textarea id="svgoutput" cols="80" rows="24"></textarea>
    </body>
</html>
"""