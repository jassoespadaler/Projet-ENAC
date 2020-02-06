N = 35     #/* Number of stations in the system */
m = 4      #/* Number of relocation vehicles */
Q = 20     #/* The capacity of a relocation vehicle */

c = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,8.000000,10922.000000,15298.000000,6736.000000,9102.000000,11040.000000,534.000000,11789.000000,12601.000000,2010.000000,12417.000000,11710.000000,13568.000000,13570.000000,11971.000000,1977.000000,13907.000000,9795.000000,936.000000,11498.000000,13551.000000,17193.000000,12315.000000,6626.000000,13842.000000,10929.000000,3285.000000,12760.000000,6321.000000,7113.000000,7037.000000,1098.000000,12156.000000,1002.000000,12526.000000],[0,10160.000000,0.000000,6171.000000,1735.000000,4085.000000,767.000000,10776.000000,1273.000000,2943.000000,9889.000000,3290.000000,2516.000000,4441.000000,4443.000000,2801.000000,11529.000000,4780.000000,6096.000000,11494.000000,1422.000000,4448.000000,8066.000000,1823.000000,2150.000000,4483.000000,3500.000000,4795.000000,3590.000000,2372.000000,1965.000000,1957.000000,10056.000000,1581.000000,9898.000000,429.000000],[0,13113.000000,4165.000000,14.000000,5494.000000,5668.000000,4283.000000,13729.000000,5032.000000,4147.000000,12842.000000,2606.000000,2962.000000,1236.000000,1749.000000,3247.000000,14482.000000,1575.000000,5433.000000,14447.000000,4331.000000,2462.000000,5501.000000,5418.000000,6087.000000,1592.000000,3884.000000,8554.000000,2041.000000,6365.000000,5560.000000,5552.000000,13009.000000,4989.000000,12851.000000,4885.000000], [0,6061.000000,2009.000000,7462.000000,2.000000,2812.000000,2058.000000,6677.000000,857.000000,3012.000000,5240.000000,4581.000000,3807.000000,5732.000000,5734.000000,3209.000000,12820.000000,6071.000000,7387.000000,12785.000000,2062.000000,5739.000000,9357.000000,1384.000000,416.000000,5774.000000,3568.000000,3425.000000,4881.000000,456.000000,1060.000000,984.000000,6197.000000,1165.000000,5799.000000,1720.000000],[0,7829.000000,3650.000000,7659.000000,2079.000000,8.000000,2530.000000,8445.000000,2136.000000,1335.000000,6136.000000,4778.000000,4004.000000,5929.000000,5931.000000,2857.000000,14105.000000,6268.000000,3440.000000,14070.000000,1560.000000,5936.000000,9554.000000,1846.000000,1993.000000,5971.000000,1891.000000,4928.000000,4705.000000,1959.000000,1522.000000,1446.000000,7551.000000,2130.000000,7567.000000,2706.000000],[0,10203.000000,774.000000,6214.000000,2103.000000,3281.000000,146.000000,10819.000000,1651.000000,2321.000000,9932.000000,3333.000000,2559.000000,4484.000000,4486.000000,1947.000000,11572.000000,4823.000000,6139.000000,11537.000000,800.000000,4491.000000,8109.000000,1887.000000,2556.000000,4526.000000,2414.000000,5163.000000,3633.000000,2834.000000,2029.000000,2021.000000,10099.000000,1458.000000,9941.000000,1354.000000],[0,1618.000000,11252.000000,15628.000000,7066.000000,9432.000000,11370.000000,8.000000,12119.000000,12931.000000,2340.000000,12747.000000,12040.000000,13898.000000,13900.000000,12325.000000,1511.000000,14237.000000,10149.000000,1266.000000,11852.000000,13905.000000,17523.000000,12669.000000,6980.000000,14281.000000,11283.000000,3639.000000,13114.000000,6675.000000,7467.000000,7391.000000,1452.000000,12510.000000,1356.000000,12880.000000],[0,10972.000000,1530.000000,7178.000000,783.000000,2836.000000,1651.000000,11588.000000,24.000000,2750.000000,5885.000000,4297.000000,3523.000000,5448.000000,5450.000000,2376.000000,12341.000000,5787.000000,6908.000000,12306.000000,1229.000000,5455.000000,9073.000000,574.000000,1243.000000,5490.000000,2843.000000,4070.000000,4224.000000,1521.000000,716.000000,708.000000,10868.000000,332.000000,10710.000000,1241.000000],[0,10872.000000,3419.000000,6655.000000,2979.000000,1598.000000,2299.000000,13121.000000,3036.000000,0.000000,7188.000000,4547.000000,2878.000000,5123.000000,5700.000000,1768.000000,12241.000000,5462.000000,2105.000000,13839.000000,1860.000000,5705.000000,9323.000000,2746.000000,2893.000000,5245.000000,556.000000,5828.000000,3204.000000,2859.000000,2422.000000,2346.000000,12401.000000,2579.000000,12243.000000,2475.000000],[0,1530.000000,9898.000000,14274.000000,5315.000000,6755.000000,10016.000000,2146.000000,5880.000000,7184.000000,12.000000,11393.000000,10686.000000,12544.000000,12546.000000,10971.000000,3789.000000,12883.000000,8795.000000,1728.000000,10498.000000,12551.000000,16169.000000,6040.000000,5229.000000,12927.000000,9929.000000,1888.000000,11760.000000,4924.000000,5716.000000,5640.000000,1426.000000,6324.000000,1268.000000,6641.000000],[0,11751.000000,3291.000000,3440.000000,4620.000000,5496.000000,3409.000000,12367.000000,4308.000000,4536.000000,11480.000000,26.000000,3645.000000,1710.000000,1712.000000,3930.000000,13120.000000,2049.000000,7687.000000,13085.000000,3457.000000,1185.000000,4803.000000,4544.000000,5213.000000,2736.000000,4629.000000,7680.000000,3924.000000,5491.000000,4686.000000,4678.000000,11647.000000,4115.000000,11489.000000,4011.000000],[0,11324.000000,2238.000000,4326.000000,3567.000000,4443.000000,2356.000000,11940.000000,3105.000000,2680.000000,11053.000000,2376.000000,50.000000,2794.000000,3332.000000,1320.000000,12693.000000,3133.000000,3966.000000,12658.000000,2404.000000,3534.000000,7152.000000,3491.000000,4160.000000,2916.000000,2417.000000,6627.000000,1486.000000,4438.000000,3633.000000,3625.000000,11220.000000,3062.000000,11062.000000,2958.000000],[0,13072.000000,4612.000000,1744.000000,5941.000000,6817.000000,4730.000000,13688.000000,5629.000000,5076.000000,12801.000000,1745.000000,3156.000000,14.000000,888.000000,3441.000000,14441.000000,353.000000,9008.000000,14406.000000,4778.000000,1601.000000,4198.000000,5865.000000,6534.000000,1489.000000,4813.000000,9001.000000,3152.000000,6812.000000,6007.000000,5999.000000,12968.000000,5436.000000,12810.000000,5332.000000],[0,13761.000000,5301.000000,2018.000000,6630.000000,7506.000000,5419.000000,14377.000000,6318.000000,5828.000000,13490.000000,2325.000000,3908.000000,766.000000,32.000000,4193.000000,15130.000000,627.000000,9697.000000,15095.000000,5467.000000,1739.000000,4042.000000,6554.000000,7223.000000,2329.000000,5565.000000,9690.000000,4042.000000,7501.000000,6696.000000,6688.000000,13657.000000,6125.000000,13499.000000,6021.000000],[0,11929.000000,2843.000000,4931.000000,3179.000000,3585.000000,1924.000000,12545.000000,2397.000000,1760.000000,11658.000000,2981.000000,1154.000000,3399.000000,3937.000000,44.000000,13298.000000,3738.000000,3296.000000,13263.000000,1546.000000,4139.000000,7757.000000,2633.000000,3302.000000,3521.000000,1747.000000,6549.000000,2532.000000,3580.000000,2775.000000,2767.000000,11825.000000,2204.000000,11667.000000,2100.000000],[0,2324.000000,11958.000000,16334.000000,7772.000000,10138.000000,12076.000000,1797.000000,12825.000000,13637.000000,3046.000000,13453.000000,12746.000000,14604.000000,14606.000000,13031.000000,58.000000,14943.000000,10855.000000,1972.000000,12558.000000,14611.000000,18229.000000,13375.000000,7686.000000,14987.000000,11989.000000,4345.000000,13820.000000,7381.000000,8173.000000,8097.000000,2158.000000,13216.000000,2062.000000,13586.000000],[0,13411.000000,4951.000000,1405.000000,6280.000000,7156.000000,5069.000000,14027.000000,5968.000000,5415.000000,13140.000000,2342.000000,3495.000000,353.000000,1227.000000,3780.000000,14780.000000,14.000000,9347.000000,14745.000000,5117.000000,1756.000000,4059.000000,6204.000000,6873.000000,1716.000000,5152.000000,9340.000000,3429.000000,7151.000000,6346.000000,6338.000000,13307.000000,5775.000000,13149.000000,5671.000000],[0,8766.000000,5559.000000,9935.000000,6888.000000,4208.000000,5677.000000,9382.000000,6426.000000,2687.000000,8495.000000,7054.000000,4234.000000,8205.000000,8207.000000,3124.000000,10135.000000,8544.000000,0.000000,10100.000000,6159.000000,8212.000000,11830.000000,6976.000000,5503.000000,5851.000000,1729.000000,6366.000000,3603.000000,5469.000000,5032.000000,4956.000000,8662.000000,6817.000000,8504.000000,7187.000000],[0,1176.000000,10615.000000,14991.000000,7007.000000,8447.000000,10733.000000,1079.000000,11482.000000,12294.000000,1703.000000,12110.000000,11403.000000,13261.000000,13263.000000,11688.000000,1443.000000,13600.000000,9512.000000,0.000000,11215.000000,13268.000000,16886.000000,12032.000000,6921.000000,13644.000000,10646.000000,3580.000000,12477.000000,6616.000000,7408.000000,7332.000000,1039.000000,11873.000000,914.000000,12243.000000],[0,11404.000000,1429.000000,6327.000000,2011.000000,2253.000000,800.000000,12020.000000,1229.000000,1899.000000,11133.000000,3446.000000,2672.000000,4597.000000,4599.000000,1525.000000,12773.000000,4936.000000,3541.000000,12192.000000,16.000000,4604.000000,8222.000000,1465.000000,2134.000000,4639.000000,1992.000000,5381.000000,3373.000000,2412.000000,1607.000000,1599.000000,10754.000000,1036.000000,10596.000000,932.000000],[0,12910.000000,4450.000000,2812.000000,5779.000000,6655.000000,4568.000000,13526.000000,5467.000000,5695.000000,12639.000000,1186.000000,4804.000000,1560.000000,1391.000000,5089.000000,14279.000000,1421.000000,8846.000000,14244.000000,4616.000000,0.000000,3618.000000,5703.000000,6372.000000,2639.000000,5788.000000,8839.000000,4556.000000,6650.000000,5845.000000,5837.000000,12806.000000,5274.000000,12648.000000,5170.000000],[0,16528.000000,8068.000000,4992.000000,9397.000000,10273.000000,8186.000000,17144.000000,9085.000000,9313.000000,16257.000000,4804.000000,7228.000000,4222.000000,4200.000000,7513.000000,17897.000000,3880.000000,12464.000000,17862.000000,8234.000000,3618.000000,0.000000,9321.000000,9990.000000,5303.000000,9406.000000,12457.000000,7016.000000,10268.000000,9463.000000,9455.000000,16424.000000,8892.000000,16266.000000,8788.000000],[0,11284.000000,1842.000000,7295.000000,567.000000,3364.000000,1891.000000,11900.000000,552.000000,3278.000000,5700.000000,4414.000000,3640.000000,5565.000000,5567.000000,2904.000000,12653.000000,5904.000000,7220.000000,12618.000000,1757.000000,5572.000000,9190.000000,20.000000,982.000000,5607.000000,3371.000000,3885.000000,4752.000000,1022.000000,1244.000000,1236.000000,11180.000000,860.000000,11022.000000,1553.000000],[0,5975.000000,2424.000000,8083.000000,416.000000,2726.000000,2556.000000,6591.000000,1243.000000,2926.000000,5154.000000,5202.000000,4428.000000,6353.000000,6355.000000,3281.000000,13235.000000,6692.000000,5031.000000,6451.000000,2134.000000,6360.000000,9978.000000,953.000000,36.000000,6395.000000,3482.000000,3339.000000,5129.000000,370.000000,629.000000,553.000000,6111.000000,1237.000000,5713.000000,2135.000000],[0,13329.000000,4211.000000,2445.000000,5540.000000,6263.000000,4329.000000,13945.000000,5078.000000,4742.000000,13058.000000,2718.000000,3008.000000,1348.000000,1861.000000,3293.000000,14698.000000,1687.000000,6028.000000,14663.000000,4377.000000,2574.000000,5613.000000,5464.000000,6133.000000,2.000000,4479.000000,8600.000000,3103.000000,6411.000000,5606.000000,5598.000000,13289.000000,5035.000000,13131.000000,4931.000000],[0,10451.000000,4747.000000,6711.000000,4762.000000,3381.000000,3627.000000,11067.000000,4100.000000,1860.000000,10180.000000,5234.000000,3407.000000,5652.000000,5882.000000,2297.000000,11820.000000,5991.000000,1684.000000,11785.000000,3249.000000,6392.000000,10010.000000,4336.000000,4676.000000,5024.000000,8.000000,7057.000000,3233.000000,4642.000000,4205.000000,4129.000000,10347.000000,3907.000000,10189.000000,3803.000000],[0,2668.000000,5074.000000,10527.000000,3459.000000,5612.000000,5123.000000,3284.000000,4024.000000,5812.000000,1847.000000,7646.000000,6872.000000,8797.000000,8799.000000,6512.000000,5205.000000,9136.000000,6454.000000,3144.000000,5365.000000,8804.000000,12422.000000,4184.000000,3373.000000,8839.000000,6368.000000,32.000000,8360.000000,3068.000000,3860.000000,3784.000000,2804.000000,4468.000000,2406.000000,4785.000000],[0,12623.000000,3537.000000,4291.000000,4866.000000,4410.000000,3715.000000,13239.000000,4188.000000,2889.000000,11386.000000,3675.000000,2334.000000,3360.000000,3898.000000,2475.000000,13026.000000,3699.000000,3587.000000,12991.000000,3337.000000,4833.000000,7229.000000,4424.000000,5093.000000,3040.000000,2626.000000,8340.000000,14.000000,5371.000000,4566.000000,4558.000000,11553.000000,3995.000000,11395.000000,3891.000000],[0,5711.000000,2602.000000,8352.000000,497.000000,2650.000000,2825.000000,6327.000000,1512.000000,2850.000000,4890.000000,5471.000000,4904.000000,6622.000000,6624.000000,3550.000000,13413.000000,6961.000000,4955.000000,6187.000000,2403.000000,6629.000000,10247.000000,1222.000000,411.000000,6664.000000,3406.000000,3075.000000,5398.000000,106.000000,898.000000,822.000000,5847.000000,1506.000000,5449.000000,2313.000000],[0,6512.000000,2222.000000,7556.000000,1027.000000,2222.000000,2029.000000,7128.000000,716.000000,2422.000000,5691.000000,4675.000000,3901.000000,5826.000000,5828.000000,2754.000000,13033.000000,6165.000000,4770.000000,12998.000000,1607.000000,5833.000000,9451.000000,426.000000,629.000000,5868.000000,3221.000000,3876.000000,4602.000000,907.000000,102.000000,94.000000,11560.000000,710.000000,6250.000000,1933.000000],[0,6436.000000,2214.000000,7548.000000,951.000000,2146.000000,2021.000000,7052.000000,708.000000,2346.000000,5615.000000,4667.000000,3893.000000,5818.000000,5820.000000,2746.000000,13025.000000,6157.000000,4451.000000,12990.000000,1599.000000,5825.000000,9443.000000,418.000000,553.000000,5860.000000,2902.000000,3800.000000,4594.000000,831.000000,94.000000,18.000000,6572.000000,702.000000,6174.000000,1925.000000],[0,1052.000000,10686.000000,15062.000000,6500.000000,8866.000000,10804.000000,955.000000,11553.000000,12365.000000,1774.000000,12181.000000,11474.000000,13332.000000,13334.000000,11759.000000,2443.000000,13671.000000,9583.000000,382.000000,11286.000000,13339.000000,16957.000000,12103.000000,6414.000000,13715.000000,10717.000000,3073.000000,12548.000000,6109.000000,6901.000000,6825.000000,42.000000,11944.000000,790.000000,12314.000000],[0,11280.000000,1838.000000,6985.000000,1114.000000,2830.000000,1458.000000,11896.000000,332.000000,2557.000000,6299.000000,4104.000000,3330.000000,5255.000000,5257.000000,2183.000000,12649.000000,5594.000000,4199.000000,12614.000000,1036.000000,5262.000000,8880.000000,568.000000,1237.000000,5297.000000,2650.000000,4484.000000,4031.000000,1515.000000,710.000000,702.000000,11176.000000,138.000000,11018.000000,1549.000000],[0,273.000000,10386.000000,14762.000000,6046.000000,8412.000000,10504.000000,657.000000,11253.000000,12065.000000,1474.000000,11881.000000,11174.000000,13032.000000,13034.000000,11459.000000,2100.000000,13371.000000,9283.000000,1059.000000,10986.000000,13039.000000,16657.000000,6771.000000,5960.000000,13415.000000,10417.000000,2619.000000,12248.000000,5655.000000,6447.000000,6371.000000,848.000000,11644.000000,10.000000,12014.000000],[0,10093.000000,651.000000,6104.000000,1980.000000,3413.000000,700.000000,10709.000000,1603.000000,2453.000000,9822.000000,3223.000000,2449.000000,4374.000000,4376.000000,2079.000000,11462.000000,4713.000000,6029.000000,11427.000000,932.000000,4381.000000,7999.000000,1839.000000,2508.000000,4416.000000,2546.000000,5040.000000,3523.000000,2786.000000,1981.000000,1973.000000,9989.000000,1410.000000,9831.000000,84.000000]];

q = [0,1, -1, 4, -5, 3, -2, -4, -4, -3, 2, 6, -3, -2, -5, -2, 17, 7, 1, -4, -5, 6, -2, 0, -5, -1, -2, 3, 14, -5, -4, -3, -2, -2, 3, -1];